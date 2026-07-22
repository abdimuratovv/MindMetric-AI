from rest_framework import serializers

from .models import TeacherReview


class TeacherReviewSerializer(serializers.ModelSerializer):
    """Validates the {rubric_scores, comment} payload from `submitReview`."""

    class Meta:
        model = TeacherReview
        fields = ['rubric_scores', 'comment', 'submitted', 'submitted_at', 'flagged']
        read_only_fields = ['submitted', 'submitted_at']
