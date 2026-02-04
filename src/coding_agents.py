import subprocess, tempfile, textwrap, os

def generate_code(question: str, previous_code=None, error=None) -> str:
    hint = ""
    if error:
        hint = f"# Fix previous error:\n# {error}\n\n"

    q = question.lower()
    if "fibonacci" in q and "prime" in q:
        return textwrap.dedent(f"""
        {hint}
        def fib(n):
            a,b=0,1
            for _ in range(n):
                a,b=b,a+b
            return a

        def is_prime(x):
            if x < 2: return False
            if x == 2: return True
            if x % 2 == 0: return False
            i=3
            while i*i <= x:
                if x % i == 0: return False
                i += 2
            return True

        def nth_prime(n):
            count=0
            x=1
            while count < n:
                x += 1
                if is_prime(x):
                    count += 1
            return x

        print("5th Fibonacci:", fib(5))
        print("25th Fibonacci:", fib(25))
        print("700th prime:", nth_prime(700))
        """).strip()

    return "print('Ask a coding question like Fibonacci + 700th prime demo')"

def execute_code(code: str):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as f:
        f.write(code)
        path = f.name

    try:
        result = subprocess.run(["python", path], capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    finally:
        try:
            os.remove(path)
        except OSError:
            pass

def solve_with_retry(question: str, max_retries: int = 3) -> str:
    code = None
    err = None

    for attempt in range(1, max_retries + 1):
        code = generate_code(question, previous_code=code, error=err)
        success, out, err_text = execute_code(code)
        if success:
            return f"[Coding Agent] Success on attempt {attempt}\n\n{out}"
        err = err_text

    return f"[Coding Agent] Failed after {max_retries} attempts.\nLast error:\n{err}"
