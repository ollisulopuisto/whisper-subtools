import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'json-to-text.py'
spec = importlib.util.spec_from_file_location('transcript_converter', SCRIPT)
converter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(converter)


class InputSafetyTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        self.content = json.dumps({'segments': [{'start': 61.9, 'text': '  Hello  '}]})

    def test_cli_preserves_input_for_common_names(self):
        for name in ['lower.json', 'upper.JSON', 'noextension', 'notes.json.backup']:
            with self.subTest(name=name):
                source = self.root / name
                source.write_text(self.content, encoding='utf-8')
                result = subprocess.run([sys.executable, str(SCRIPT), str(source)],
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(source.read_text(encoding='utf-8'), self.content)
                self.assertEqual(source.with_suffix('.md').read_text(encoding='utf-8'),
                                 '**00:01:01** Hello\n\n')

    def test_cli_rejects_input_already_named_markdown(self):
        source = self.root / 'input.md'
        source.write_text(self.content, encoding='utf-8')
        result = subprocess.run([sys.executable, str(SCRIPT), str(source)],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('different from the input', result.stderr)
        self.assertEqual(source.read_text(encoding='utf-8'), self.content)

    def test_function_rejects_same_path_and_aliases(self):
        source = self.root / 'input.json'
        source.write_text(self.content, encoding='utf-8')
        symlink = self.root / 'symlink.md'
        symlink.symlink_to(source)
        hardlink = self.root / 'hardlink.md'
        hardlink.hardlink_to(source)
        for output in [source, source.parent / '.' / source.name, symlink, hardlink]:
            with self.subTest(output=output):
                with self.assertRaises(ValueError):
                    converter.transcript_to_text(source, output)
                self.assertEqual(source.read_text(encoding='utf-8'), self.content)


if __name__ == '__main__':
    unittest.main()
