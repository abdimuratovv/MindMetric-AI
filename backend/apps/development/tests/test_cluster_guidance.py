from django.test import SimpleTestCase, TestCase, override_settings
from unittest.mock import patch
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.assessments.models import AssessmentAttempt
from apps.scoring.models import IndicatorScore
from apps.development.cluster_guidance import CLUSTER_INDICATORS, cluster_guidance


KEYS = {key for group in CLUSTER_INDICATORS.values() for key in group}


class ClusterGuidancePolicyTests(SimpleTestCase):
    def test_mapping_partitions_all_ten_indicators(self):
        from apps.scoring.constants import INDICATOR_CHOICES
        self.assertEqual(KEYS, {key for key, _ in INDICATOR_CHOICES})
        self.assertEqual(sum(map(len, CLUSTER_INDICATORS.values())), 10)

    def test_each_cluster_can_be_recommended_with_real_evidence(self):
        for number, group in CLUSTER_INDICATORS.items():
            scores = dict.fromkeys(KEYS, 90)
            scores.update(dict.fromkeys(group, 40))
            for lang in ('uz', 'ru'):
                result = cluster_guidance(scores, KEYS, lang)
                selected = [r for r in result['clusters'] if r['recommended']]
                self.assertEqual([r['id'] for r in selected], [number])
                self.assertEqual(selected[0]['score'], 40)
                self.assertEqual({r['key'] for r in selected[0]['indicators']}, set(group))
                self.assertIn('40/100', selected[0]['reason'])

    def test_equal_scores_keep_all_ties_and_high_results_are_maintenance(self):
        for value in (0, 55, 80, 100):
            result = cluster_guidance(dict.fromkeys(KEYS, value), KEYS)
            self.assertTrue(all(row['recommended'] for row in result['clusters']))
            self.assertEqual(result['mode'], 'maintenance' if value >= 80 else 'development')

    def test_partial_retake_missing_and_invalid_scores_do_not_recommend(self):
        scores = dict.fromkeys(KEYS, 75)
        self.assertFalse(cluster_guidance(scores, KEYS - {'attention'})['available'])
        for value in (None, float('nan'), float('inf'), -1, 101, True):
            self.assertFalse(cluster_guidance({**scores, 'attention': value}, KEYS)['available'])
        self.assertFalse(cluster_guidance({}, set())['available'])

    def test_average_uses_cluster_size_and_shared_ties(self):
        scores = dict.fromkeys(KEYS, 80)
        scores.update(math=30, logic=60, iq=90, algorithmic=60, creative=60, problem_solving=60)
        result = cluster_guidance(scores, KEYS)
        self.assertEqual([r['id'] for r in result['clusters'] if r['recommended']], [1, 2])


class ClusterGuidanceAPITests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user('guidance@example.com')
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        for key in KEYS:
            AssessmentAttempt.objects.create(student=self.user, assessment_type=key, status='completed')
            IndicatorScore.objects.create(student=self.user, indicator_key=key, score=40 if key in CLUSTER_INDICATORS[3] else 90)

    def test_summary_localized_owned_readonly_and_retake_safe(self):
        before = list(IndicatorScore.objects.values_list('pk', 'score'))
        for lang in ('uz', 'ru'):
            response = self.client.get('/api/results/summary/', HTTP_X_LANGUAGE=lang)
            self.assertEqual(response.status_code, 200)
            result = response.data['clusterRecommendation']
            self.assertEqual([r['id'] for r in result['clusters'] if r['recommended']], [3])
        self.assertEqual(before, list(IndicatorScore.objects.values_list('pk', 'score')))
        AssessmentAttempt.objects.filter(student=self.user, assessment_type='attention').update(status='in_progress')
        self.assertFalse(self.client.get('/api/results/summary/').data['clusterRecommendation']['available'])
        other = get_user_model().objects.create_user('guidance-other@example.com')
        self.client.force_authenticate(other)
        self.assertFalse(self.client.get('/api/results/summary/').data['clusterRecommendation']['available'])
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get('/api/results/summary/').status_code, 401)

    @override_settings(DEVELOPMENT_CLUSTER1_ENABLED=True)
    def test_plan_uses_same_policy_and_hides_guidance_during_check(self):
        from apps.accounts.models import StudentProfile
        from django.utils import timezone
        StudentProfile.objects.create(user=self.user, completed_at=timezone.now())
        expected = self.client.get('/api/results/summary/').data['clusterRecommendation']
        self.assertEqual(self.client.get('/api/development/plan/').data['clusterRecommendation'], expected)
        with patch('apps.development.views.build_plan', return_value={
            'recommended': [], 'entries': [], 'check_active': True, 'active_enrollment_id': 1,
            'minimum_diagnostic_responses': 3,
        }):
            self.assertIsNone(self.client.get('/api/development/plan/').data['clusterRecommendation'])
