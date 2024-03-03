#ifndef __FRANKENSTEIN_SKELETON_CONSTANTS__
#define __FRANKENSTEIN_SKELETON_CONSTANTS__

#define TOOL_SELECT_JOINT      0
#define TOOL_ADD_JOINT         1
#define TOOL_MOVE_JOINT        2
#define TOOL_INSERT_JOINT      3
#define TOOL_REMOVE_JOINT      4
#define TOOL_PARENT_JOINT      5
#define TOOL_UNPARENT_JOINT    6
#define TOOL_ORIENT_JOINT      7

#define FUNC_VOID       0
#define FUNC_RENAME     1
#define FUNC_REMOVE     2

#define PROJECTION_FREE             0
#define PROJECTION_PLANE            1
#define PROJECTION_SURFACE          2
#define PROJECTION_SURFACE_DEPTH    3

#define GEO_SKELETON     0
#define GEO_CONSTRUCTION 1
#define GEO_SKIN         2

#define PTOOL       "../tool"

#define PFUNCTIONS  "../functions"

#define PVS_TOOL_STATE          "../vs_toolState"
#define PVS_JOINT_ID            "../vs_jointID"
#define PVS_JOINT_PRIMID        "../vs_jointPrimID"
#define PVS_JOINT_PRIMUVW       "../vs_jointPrimUVW"
#define PVS_JOINT_PARENTID      "../vs_jointParentID"
#define PVS_RAY_ORIGIN          "../vs_rayOrigin"
#define PVS_RAY_DIRECTION       "../vs_rayDirection"
#define PVS_JOINT_SELECTION     "../vs_jointSelection"
#define PVS_JOINT_HIGHLIGHT     "../vs_jointHighlight"
#define PVS_ORIENT_PRIM         "../vs_orientPrim"
#define PVS_ORIENT_TARGET_PRIM  "../vs_orientTargetPrim"
#define PVS_ORIENT_JOINTID      "../vs_orientJointID"
#define PVS_ORIENT_AXIS         "../vs_orientAxis"
#define PVS_ORIENT_TARGETJOINTID "../vs_orientTargetJointID"
#define PVS_ORIENT_TARGETAXIS   "../vs_orientTargetAxis"
#define PVS_SKINPOINTHIGHLIGHT  "../vs_skinPointHighlight"
#define PVS_SKINPOINTSELECTION  "../vs_skinPointsSelection"
#define PVS_SKINHIGHLIGHT       "../vs_skinHighlight"
#define PVS_SKINSELECTION       "../vs_skinSelection"
#define PVS_LIVE                "../vs_live"
#define PVS_SKINPOINTID         "../vs_skinPointID"
#define PVS_SKINPRIMID          "../vs_skinPrimID"
#define PVS_SKINPRIMUVW         "../vs_skinPrimUVW"

#define PNAMING_BASE            "../naming_base"
#define PNAMING_PART            "../naming_part"
#define PNAMING_PREFIX_MIDDLE   "../naming_prefixMiddle"
#define PNAMING_PREFIX_LEFT     "../naming_prefixLeft"
#define PNAMING_PREFIX_RIGHT    "../naming_prefixRight"

#define PPROJECTION_TYPE                "../projection_type"
#define PPROJECTION_PLANE_ORIENT        "../projection_planeOrient"
#define PPROJECTION_PLANE_ORIGIN        "../projection_planeOrigin"
#define PPROJECTION_PLANE_TOFLOOR       "../projection_planeToFloor"
#define PPROJECTION_PLANE_SCALE         "../projection_planeScale"
#define PPROJECIONT_PLANE_OFFSETPOS     "../projection_planeOffsetPos"
#define PPROJECIONT_PLANE_OFFSETROT     "../projection_planeOffsetRot"
#define PPROJECIONT_PLANE_OFFSETSCL     "../projection_planeOffsetScl"
#define PPROJECTION_SURFACEDEPTH_MIX    "../projection_surfaceDephtMix"
#define PPROJECTION_SNAPPOINT           "../projection_snapPoint"
#define PPROJECTION_RAYTYPE             "../projection_rayType"
#define PPROJECTION_DEPTHTYPE           "../projection_depthType"

#define PINSERT_TYPE                    "../insert_type"
#define PINSERT_LOCATION                "../insert_snapLocation"
#define PINSERT_MULTI_COUNT             "../insert_multiJointCount"

#define PORIENT_LOCKAXIS                "../orient_lockAxis"
#define PORIENT_SNAPTOJOINT             "../orient_snapToJoint"
#define PORIENT_SNAPTOSKIN              "../orient_snapToSkinPoint"
#define PORIENT_SNAPTOAXIS              "../orient_SnapToJointAxis"
#define PORIENT_RULE_MAINAXIS           "../orient_ruleMainAxis"
#define PORIENT_RULE_SECONDARYAXIS      "../orient_ruleSecondaryAxis"
#define PORIENT_DISPLAY_SCALE           "../orient_displayScale"

#define PCOLOR_MIDDLE                   "../color_middle"
#define PCOLOR_LEFT                     "../color_left"
#define PCOLOR_RIGHT                    "../color_right"
#define PCOLOR_SELECTED                 "../color_selected"
#define PCOLOR_HIGHLIGHT                "../color_highlight"
#define PCOLOR_HELPER                   "../color_helper"
#define PCOLOR_PLANE                    "../color_plane"
#define PCOLOR_DISABLE                  "../color_disable"

#define ATTRIB_HELPER           "helper"
#define ATTRIB_MOVED            "moved"
#define ATTRIB_MAIN_AXIS        "mainAxis"
#define ATTRIB_UP_AXIS          "upAxis"
#define ATTRIB_TRANSFORM        "transform"
#define ATTRIB_NAME             "name"
#define ATTRIB_PREFIX_SIDE      "prefixSide"
#define ATTRIB_PART             "part"
#define ATTRIB_BASE_NAME        "baseName"
#define ATTRIB_SYMID            "symID"
#define ATTRIB_SKINGEO_CENTER   "skinGeometryCenter"
#define ATTRIB_SKINGEO_SIZE     "skinGeometrySize"

#endif