#!/usr/bin/env python
"""This modules contains tests for artifact API renderer."""



# pylint: disable=unused-import,g-bad-import-order
from grr.lib import server_plugins
# pylint: enable=unused-import,g-bad-import-order

from grr.gui.api_plugins import artifact as artifact_plugin

from grr.lib import artifact_lib
from grr.lib import artifact_test
from grr.lib import flags
from grr.lib import test_lib
from grr.lib import utils


class ArtifactRegistryMock(object):

  class Artifacts(object):

    def items(self):
      return {}

  artifacts = Artifacts()


class ArtifactRendererTest(artifact_test.ArtifactBaseTest):
  """Test for ArtifactRendererTest."""

  def setUp(self):
    super(ArtifactRendererTest, self).setUp()
    self.renderer = artifact_plugin.ApiArtifactRenderer()
    self.LoadTestArtifacts()

  def _renderEmptyArtifacts(self):
    with utils.Stubber(artifact_lib, "ArtifactRegistry", ArtifactRegistryMock):
      mock_request = utils.DataObject(token="")
      rendering = self.renderer.Render(mock_request)
    return rendering

  def testNoArtifacts(self):
    rendering = self._renderEmptyArtifacts()
    self.assertEqual(rendering, {})
    self.assertFalse(rendering)

  def _renderTestArtifacts(self):
    mock_request = utils.DataObject(token="")
    rendering = self.renderer.Render(mock_request)
    return rendering

  def testPrepackagedArtifacts(self):
    rendering = self._renderTestArtifacts()

    # we know there are some prepackaged artifacts
    self.assertTrue(rendering)

    # test for a prepackaged artifact we know to exist
    self.assertIn("FakeArtifact", rendering)
    self.assertIn("custom", rendering["FakeArtifact"])
    self.assertIn("processors", rendering["FakeArtifact"])
    self.assertFalse(rendering["FakeArtifact"]["custom"])

    for required_key in ("doc",
                         "labels",
                         "supported_os"):
      self.assertIn(required_key, rendering["FakeArtifact"]["artifact"])


def main(argv):
  test_lib.main(argv)


if __name__ == "__main__":
  flags.StartMain(main)
