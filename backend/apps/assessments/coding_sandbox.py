"""
Real JS execution for the coding phase — replaces the old RunCodingView/SubmitCodingView
stub that marked every submission as fully passing regardless of what was submitted.

Runs student-submitted code in py_mini_racer's embedded V8 isolate, inside a dedicated
subprocess. MiniRacer's `timeout` kwarg normally interrupts a runaway script (e.g. an
infinite loop), but pathological/malformed input can still hang or crash the V8 layer
itself outright — observed directly while building this against genuinely malformed
input (a syntax-mangled submission wedged one function declaration inside a `//`
comment on top of another) took down the whole dev server process, not just the
request. Running the eval in its own process means that failure only kills the
submission's subprocess; the Django worker handling every other student's requests is
unaffected. `timeout` alone (no subprocess) is not enough for untrusted code.
"""
import json
import multiprocessing

EVAL_TIMEOUT_MS = 2000
PROCESS_TIMEOUT_SECONDS = 5


def _evaluate(function_name: str, code: str, cases: list, result_queue) -> None:
    """Runs in the child process — imported/called fresh each time, so a crash here
    never touches the parent's already-loaded Django/MiniRacer state."""
    from py_mini_racer import MiniRacer

    ctx = MiniRacer()
    try:
        ctx.eval(code, timeout=EVAL_TIMEOUT_MS)
    except Exception:
        result_queue.put([{'label': c['label'], 'passed': False} for c in cases])
        return

    results = []
    for c in cases:
        try:
            call = f'{function_name}({json.dumps(c["input"])})'
            actual = ctx.eval(call, timeout=EVAL_TIMEOUT_MS)
        except Exception:
            results.append({'label': c['label'], 'passed': False})
            continue
        results.append({'label': c['label'], 'passed': actual == c['expected']})
    result_queue.put(results)


def run_test_cases(function_name: str, code: str, cases: list) -> list:
    """
    Evaluates `code` (expected to define `function_name`) once, then calls that
    function with each case's `input` and compares the result to `expected`.

    Returns [{'label', 'passed'}] in `cases` order. A case whose call errors or
    times out fails just that case; `code` that fails to even parse/eval, hangs
    past PROCESS_TIMEOUT_SECONDS, or crashes the subprocess outright fails every
    case rather than raising out of the view or taking the server down with it.
    """
    ctx = multiprocessing.get_context('spawn')
    result_queue = ctx.Queue()
    process = ctx.Process(target=_evaluate, args=(function_name, code, cases, result_queue))
    process.start()
    process.join(PROCESS_TIMEOUT_SECONDS)
    if process.is_alive():
        process.terminate()
        process.join()

    if not result_queue.empty():
        return result_queue.get()
    return [{'label': c['label'], 'passed': False} for c in cases]
