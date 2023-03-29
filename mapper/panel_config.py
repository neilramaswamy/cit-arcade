# A PanelConfig records all the metadata about a display (i.e. a collection of panels). It is
# serialized to the filesystem so that we can reuse it without having to run another recalibration.
class PanelConfig():
    def __init__(self,
                 horz_side_length: int, vert_side_length: int,
                 horz_panels: int, vert_panels: int,
                 mapping: dict[int, int]):
        self.horz_side_length = horz_side_length
        self.vert_side_length = vert_side_length
        self.horz_panels = horz_panels
        self.vert_panels = vert_panels
        self.mapping = mapping