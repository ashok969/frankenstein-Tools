
class SkeletonTool(object):

    SelectJoints    = 0
    AddJoint        = 1
    MoveJoint       = 2
    InsertJoint     = 3
    RemoveJoint     = 4
    ParentJoint     = 5
    UnParentJoint   = 6
    OrientJoint     = 7
    RenameJoint     = 8

    StringValues    = [
        "Select Joint",
        "Add Joint",
        "Move Joint",
        "Insert Joint",
        "Remove Joint",
        "Parent Joint",
        "UnParent Joint",
        "Orient Joint",
        "Rename Joint"
    ]

    KeyValues       = [
        "1", "2", "3", "4", "5", "6", "7", "8", "9"
    ]

class SkeletonProjectionType(object):

    Free                = 0
    ConstructionPlane   = 1
    Surface             = 2
    SurfaceDepth        = 3

    StringValues    = [
        "Free",
        "Plane",
        "Surface",
        "Surface Depth"
    ]

    KeyValues       = [
        "z", "x", "c", "v"
    ]

class SkeletonProjectionRayType(object):

    Ray         = 0
    SkinNormal  = 1

    StringValues = [
        "Ray",
        "Skin Normal"
    ]

class SkeletonProjectionDepthType(object):

    FirstTwo    = 0
    All         = 1

    StringValues = [
        "First Two",
        "All"
    ]

class SkeletonProjectionOrient(object):

    XY  = 0
    YZ  = 1
    ZX  = 2

    StringValues = ["XY", "YZ", "ZX"]

    KeyValues = ["d", "f", "g"]

class SkeletonToolState(object):

    Disable     = 0
    Enable      = 1

    StringValues    = [
        "Disable",
        "Enable"
    ]

class SkeletonFunctions(object):

    Void                    = 0
    RenameJoints            = 1
    RemoveSelectedJoints    = 2
    SymmetrizeSkeleton      = 3
    DisableJoints           = 4
    EnableJoints            = 5
    ResetDisable            = 6
    NormalizeJoints         = 7
    ResetJointsOrientation  = 8

    StringValues = [
        "Void",
        "Rename Joints",
        "Remove Selected Joints",
        "Symmetrize Skeleton",
        "Disable Joints",
        "Enable Joints",
        "Reset Disable",
        "Normalize Joints",
        "Reset Joints Orientation"
    ]

class SkeletonSelectionHierarchy(object):

    All         =  0
    Branch      = 1

    StringValues = [
        "All",
        "Branch"
    ]

    KeyValues = ["b", "b"]

class SkeletonSelectionType(object):

    Joint       = 0
    Skin        = 1

    StringValues = ["Joint", "Skin"]

    KeyValue = ["f", "g"]

class SkeletonInsertType(object):

    Free        = 0
    Snapped     = 1
    Multi       = 2

    StringValues = ["Free", "Snapped", "Multi"]

    KeyValues   = ["d", "f", "g"]

class SkeletonLockAxis(object):

    Free        = 0
    X           = 1
    Y           = 2
    Z           = 3

    StringValues = ["Free", "X", "Y", "Z"]

    KeyValues = ["z", "x", "c", "v"]
