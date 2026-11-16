"""Unit tests for the agent-docs Handlebars shim (task 3.1). Run: python3 -m unittest test_render.py"""
import importlib.util
import pathlib
import unittest

spec = importlib.util.spec_from_file_location("render", pathlib.Path(__file__).with_name("render.py"))
render_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(render_mod)
render = render_mod.render


class RenderTest(unittest.TestCase):
    def test_doc_link(self):
        self.assertEqual(render('{{{docLink "../model/README.md" "Model docs" "judo-model-docs"}}}', "<app>"),
                         "[Model docs](../model/README.md)")

    def test_doc_link_without_skill(self):
        self.assertEqual(render('{{{docLink "a.md" "A"}}}', "<app>"), "[A](a.md)")

    def test_local_hub_link(self):
        self.assertEqual(render('{{{localHubLink "Back" "judo-backend"}}}', "<app>"), "[Back](./README.md)")

    def test_lower_case_model_name(self):
        out = render("cd application/{{ lowerCase model.name }}", "<app>")
        self.assertNotIn("{{", out)
        self.assertIn("<app>", out)

    def test_no_helpers_left(self):
        src = '{{{docLink "x.md" "X" "s"}}} and {{{localHubLink "H" "s"}}} and {{ lowerCase model.name }}'
        self.assertNotRegex(render(src, "<app>"), r"\{\{\{?\s*(docLink|localHubLink|lowerCase)")


if __name__ == "__main__":
    unittest.main()
