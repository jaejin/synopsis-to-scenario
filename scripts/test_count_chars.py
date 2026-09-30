"""count_chars.py 단위 테스트 — 실행: python -m unittest scripts/test_count_chars.py"""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from count_chars import count_body_chars  # noqa: E402

SCRIPT = Path(__file__).parent / "count_chars.py"


class 공백제외_글자수_집계(unittest.TestCase):

    def test_공백과_줄바꿈을_모두_뺀다(self):
        # given
        text = "가 나\t다\n라　마"  # 전각 공백 포함
        # when
        actual = count_body_chars(text)
        # then
        self.assertEqual(5, actual)

    def test_첫_제목_줄은_제외한다(self):
        # given
        text = "# 제1화 — 시작\n\n본문입니다."
        # when
        actual = count_body_chars(text)
        # then
        self.assertEqual(len("본문입니다."), actual)

    def test_두번째_제목_줄부터는_본문으로_센다(self):
        # given
        text = "# 제1화\n# 둘째\n본문"
        # when
        actual = count_body_chars(text)
        # then
        self.assertEqual(len("#둘째본문"), actual)

    def test_장면_전환_기호_줄은_제외한다(self):
        # given
        text = "앞\n***\n* * *\n---\n◆\n뒤"
        # when
        actual = count_body_chars(text)
        # then
        self.assertEqual(2, actual)

    def test_HTML_주석은_여러_줄이어도_제외한다(self):
        # given
        text = "본문<!-- 메모\n떡밥 A 심기 -->끝"
        # when
        actual = count_body_chars(text)
        # then
        self.assertEqual(len("본문끝"), actual)

    def test_문장부호와_따옴표는_센다(self):
        # given
        text = "\"뭐?\" 그가 물었다…!"
        # when
        actual = count_body_chars(text)
        # then
        self.assertEqual(len("\"뭐?\"그가물었다…!"), actual)


class 명령줄_판정(unittest.TestCase):

    def _run(self, *args):
        return subprocess.run([sys.executable, str(SCRIPT), *args],
                              capture_output=True, text=True, encoding="utf-8")

    def _write(self, directory, name, chars):
        path = Path(directory) / name
        path.write_text("# 제목\n" + "가" * chars, encoding="utf-8")
        return path

    def test_범위_안이면_종료코드_0(self):
        with tempfile.TemporaryDirectory() as d:
            # given
            self._write(d, "ep_001.md", 5000)
            # when
            actual = self._run(d)
            # then
            self.assertEqual(0, actual.returncode, actual.stdout)
            self.assertIn("통과 1개", actual.stdout)

    def test_미달과_초과가_있으면_종료코드_1(self):
        with tempfile.TemporaryDirectory() as d:
            # given
            self._write(d, "ep_001.md", 4799)
            self._write(d, "ep_002.md", 5501)
            # when
            actual = self._run(d)
            # then
            self.assertEqual(1, actual.returncode)
            self.assertIn("미달 회차: ep_001.md", actual.stdout)
            self.assertIn("초과 회차: ep_002.md", actual.stdout)

    def test_경계값은_통과로_본다(self):
        with tempfile.TemporaryDirectory() as d:
            # given
            self._write(d, "ep_001.md", 4800)
            self._write(d, "ep_002.md", 5500)
            # when
            actual = self._run(d)
            # then
            self.assertEqual(0, actual.returncode, actual.stdout)

    def test_min_max_옵션으로_범위를_바꾼다(self):
        with tempfile.TemporaryDirectory() as d:
            # given
            path = self._write(d, "ep_001.md", 3000)
            # when
            actual = self._run(str(path), "--min", "2900", "--max", "3100")
            # then
            self.assertEqual(0, actual.returncode, actual.stdout)

    def test_회차_파일이_없으면_종료코드_1(self):
        with tempfile.TemporaryDirectory() as d:
            # when
            actual = self._run(d)
            # then
            self.assertEqual(1, actual.returncode)
            self.assertIn("검사할 회차 파일이 없습니다", actual.stderr)

    def test_없는_경로는_경고한다(self):
        # when
        actual = self._run("/존재하지/않는/경로")
        # then
        self.assertEqual(1, actual.returncode)
        self.assertIn("경로를 찾을 수 없습니다", actual.stderr)


if __name__ == "__main__":
    unittest.main()
