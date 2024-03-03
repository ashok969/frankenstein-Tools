
HUD_PROJECTION_CONSTRUCTION_PLANE = {
    "id" : "constructionPlaneInfos", "type" : "group",
    "rows" : [
        {"id" : "planeOrient", "label" : "Construction Plane Orientation", "value" : "XY", "key": "D / F / G"},
        {"id" : "planeOrient_g", "type" : "choicegraph", "count" : 3},
        {"id" : "planeOrigin", "label" : "Origin", "value" : "World"},
        {"id" : "planeGlobalScale", "label": "Plane Scale", "value" : "1.0", "key" : "mousewheel"},
    ]
}

HUD_PROJECTION_SURFACE_DEPTH = {
    "id" : "surfaceDepthInfos", "type" : "group",
    "rows" : [
        {"id": "surfaceDepthRayType", "label": "Ray Type", "value": "Ray", "key": "F"},
        {"id": "surfaceDepthDepthType", "label": "Depth Type", "value": "First Two", "key": "G"},        
        {"id": "surfaceDepthMix", "label" : "Mix From Back", "value" : "0.5", "key" : "mousewheel"}
    ]
}

HUD_PROJECTION_SURFACE = {
    "id": "surfaceInfos", "type": "group",
    "rows" : [
        {"id": "surfaceSnapPoint", "label": "Snap To Point", "value": "Off", "key": "D"}
    ]
}
HUD_PROJECTION_SURFACE["rows"].append(HUD_PROJECTION_SURFACE_DEPTH)

HUD_PROJECTION_TYPE = {
    "id"    : "projectionTypeInfos", "type"  : "group",
    "rows"  : [
        {"id" : "projectionType", "label" : "Projection Type", "value" : "Free", "key" : "Z / X / C / V"},
        {"id" : "projectionType_g", "type": "choicegraph", "count" : 4},
        {"id" : "projectionToolSep", "type" : "divider"}
    ]
}

HUD_PROJECTION_TYPE["rows"].append(HUD_PROJECTION_CONSTRUCTION_PLANE)
HUD_PROJECTION_TYPE["rows"].append(HUD_PROJECTION_SURFACE) 


HUD_SELECT_JOINTS = {
    "id": "selectJointInfos", "type" : "group",
    "rows" : [
        {"id": "select", "label": "Select", "key":"LMB"},
        {"id": "addSelect", "label": "Add To Selection", "key": "Shift + LMB"},
        {"id": "removeSelect", "label": "Remove From Selection", "key": "Ctrl + LMB"},
        {"id": "selectHierarchy", "label": "Select Hierarchy", "key": "Double + LMB"},
        {"id": "addSelectHierarchy", "label": "Add Hierarchy To Selection", "key" : "Shift + Double + LMB"},
        {"id": "removeSelectHierarchy", "label": "Remove Hierarchy From Selection", "key" : "Ctrl + Double + LMB"},
        {"id": "selHierarchyBehavior", "label": "Toggle Select Hierarchy Behavior", "key": "B", "value": "All"}
    ]
}

HUD_SELECT_SKIN = {
    "id": "selectSkinInfos", "type" : "group",
    "rows" : [
        {"id": "select", "label": "Select", "key":"LMB"},
        {"id": "addSelect", "label": "Add To Selection", "key": "Shift + LMB"},
        {"id": "removeSelect", "label": "Remove From Selection", "key": "Ctrl + LMB"},
    ]

}

HUD_SELECT = {
    "id" : "selectInfos", "type": "group",
    "rows" : [
        {"id": "selectionType", "label": "Selection Type", "key": "F / G", "value": "Joint"},
        {"id": "selectionType_g", "type": "choicegraph", "count": 2},
        {"id": "selectionSep", "type": "divider"}
    ]
}

HUD_SELECT["rows"].append(HUD_SELECT_JOINTS)
HUD_SELECT["rows"].append(HUD_SELECT_SKIN)



HUD_INSERT_JOINT = {
    "id": "insertJointActions", "type": "group",
    "rows" : [
        {"id": "insertJointSep", "type": "divider"},
        {"id": "insertJoint", "label": "Insert Joint", "key": "LMB"}
    ] 
}

HUD_INSERT_SNAPPED = {
    "id": "insertSnappedInfos", "type": "group",
    "rows" : [
        {"id": "snapLocation", "label": "Snap Location", "key": "mousewheel", "value": "0.5"},
    ]
}

HUD_INSERT_MULTI = {
    "id": "insertMultiInfos", "type": "group",
    "rows": [
        {"id": "jointCount", "label": "Joint Count", "key": "mousewheel", "value": "2"},
    ]
}

HUD_INSERT = {
    "id": "insertJointInfos", "type": "group",
    "rows": [
        {"id": "insertType", "label": "Insert Type", "key": "D / F / G", "value": "Free"},
        {"id": "insertType_g", "type": "choicegraph", "count": 3},
        {"id": "insertSep", "type": "divider"}    
    ]
}

HUD_INSERT["rows"].append(HUD_INSERT_SNAPPED)
HUD_INSERT["rows"].append(HUD_INSERT_MULTI)
HUD_INSERT["rows"].append(HUD_INSERT_JOINT)


HUD_ORIENT = {
    "id": "orientJointInfos", "type": "group",
    "rows" : [
        {"id": "lockAxis", "label": "Lock Axis", "key": "Z / X / C / V", "value": "Free"},
        {"id": "lockAxis_g", "type": "choicegraph", "count": 4},
        {"id": "snapToJoint", "label": "Snap To Joint", "key": "D", "value": "Enable"},
        {"id": "snapToJointAxis", "label": "Snap To Joint Axis", "key": "F", "value": "Enable"},
        {"id": "snapToSkinPoint", "label": "Snap To Skin Point", "key": "G", "value": "Enable"},
        {"id": "orientDisplayScale", "label": "Display Scale", "key": "mousewheel", "value": "1.0"}    
    ]
}

HUD_MOVE = {
    "id": "moveInfos", "type": "group",
    "rows" : [
        {"id": "MoveSep", "type": "divider"},
        {"id": "moveJoint", "label": "Move Joint", "key": "LMB + drag"}
    ]
}

HUD_ADD = {
    "id": "addInfos", "type": "group",
    "rows" : [
        {"id": "addSep", "type": "divider"},
        {"id": "addJoint", "label": "Add Joint", "key": "LMB + drag"},
        {"id": "endChain", "label": "End Chain", "key": "B"}
    ]
}

HUD_REMOVE = {
    "id": "removeInfos", "type": "group",
    "rows" : [
        {"id": "removeJoint", "label": "Remove Joint", "key": "LMB"}
    ]
}

HUD_PARENT = {
    "id": "parentInfos", "type": "group",
    "rows" : [
        {"id": "parentJoint", "label": "Parent Joint\n Click the parent joint and drag to child joint.", "key": "LMB + drag"}
    ]
}

HUD_UNPARENT = {
    "id": "unParentInfos", "type": "group",
    "rows" : [
        {"id": "unParentJoint", "label": "Unparent Joint\n Click Joint connection shape.", "key": "LMB"}
    ]
}

HUD_TOOLS = {
    "id" : "toolInfos", "type" : "group",
    "rows" : [
        {"id": "tool", "label": "Tool", "key": "1-8", "value": "Add Joint"},
        {"id": "tool_g", "type": "choicegraph", "count": 8},
        {"id": "toolSep", "type": "divider"}
    ]
}


HUD_TEMPLATE = {
    "title" : "Frankenstein Skeleton Builder",
    "desc"  : "tool",
    "icon"  : "SOP_kinefx-skeleton",
    "rows"  : [
    ]
}

HUD_TEMPLATE["rows"].append(HUD_TOOLS)
HUD_TEMPLATE["rows"].append(HUD_SELECT)
HUD_TEMPLATE["rows"].append(HUD_PROJECTION_TYPE)
HUD_TEMPLATE["rows"].append(HUD_ADD)
HUD_TEMPLATE["rows"].append(HUD_MOVE)
HUD_TEMPLATE["rows"].append(HUD_INSERT)
HUD_TEMPLATE["rows"].append(HUD_REMOVE)
HUD_TEMPLATE["rows"].append(HUD_ORIENT)
HUD_TEMPLATE["rows"].append(HUD_PARENT)
HUD_TEMPLATE["rows"].append(HUD_UNPARENT)