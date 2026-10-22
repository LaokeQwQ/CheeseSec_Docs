import importlib.util
import tempfile
import unittest
from pathlib import Path


SPEC = importlib.util.spec_from_file_location("handbook", Path(__file__).resolve().parents[1] / "scripts/sync_plugin_handbook.py")
handbook = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handbook)


class PublicBoundaryTests(unittest.TestCase):
    def prepare(self, root):
        for name in handbook.PUBLIC_INPUTS:
            path = root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{"title": "Plugins"}\n\nPublic plugin overview.\n')

    def test_unlisted_source_is_never_imported(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prepare(root)
            (root / "handbook/public/internal.md").write_text("Do not publish")
            generated = handbook.synchronize(root)
            self.assertEqual(set(generated), {*handbook.PUBLIC_INPUTS.values(), "data/plugin_handbook.json"})
            self.assertFalse(any(b"Do not publish" in data for data in generated.values()))
            handbook.synchronize(root, check=True)

    def test_deployment_detail_is_rejected_before_outputs_are_written(self):
        for marker in ("Cloudflare", "bucket", "127.0.0.1", "publish_r2.sh"):
            with self.subTest(marker=marker), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.prepare(root)
                (root / next(iter(handbook.PUBLIC_INPUTS))).write_text('{"title": "Plugins"}\n' + marker)
                with self.assertRaisesRegex(ValueError, "deployment detail"):
                    handbook.synchronize(root)
                self.assertFalse((root / "content").exists())

    def test_old_page_or_raw_download_fails_closed(self):
        for name in ("content/docs/plugins/internal.md", "static/plugins/reference/private.json"):
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.prepare(root)
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("old content")
                with self.assertRaisesRegex(ValueError, "unreviewed"):
                    handbook.synchronize(root)

    def test_source_symlink_and_changed_output_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.prepare(root)
            handbook.synchronize(root)
            (root / next(iter(handbook.PUBLIC_INPUTS.values()))).write_text("stale")
            with self.assertRaisesRegex(ValueError, "stale"):
                handbook.synchronize(root, check=True)
            source = root / next(iter(handbook.PUBLIC_INPUTS))
            source.unlink()
            source.symlink_to(root / "handbook/public/overview.zh.md")
            with self.assertRaisesRegex(ValueError, "symlink"):
                handbook.synchronize(root)


if __name__ == "__main__":
    unittest.main()
