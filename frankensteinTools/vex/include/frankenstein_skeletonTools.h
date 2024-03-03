#ifndef __FRANKENSTEIN_SKELETON_TOOLS__
#define __FRANKENSTEIN_SKELETON_TOOLS__

#include <frankenstein_skeleton.h>
#include <frankenstein_skeletonConstants.h>
#include <frankenstein_projectionTools.h>
#include <frankenstein_jointOrient.h>


string
jointNaming(
    const string    sidePrefix;
    const string    baseName
)
{
    return sprintf("%s_%s", sidePrefix, baseName);
}

string
jointNaming(
    const string    sidePrefix;
    const string    baseName;
    const int       index  
)
{
    return sprintf("%s_%s_%i", sidePrefix, baseName, index);
}

string
jointNaming(
    const string    sidePrefix;
    const string    partPrefix;
    const string    baseName;
)
{
    return sprintf("%s_%s_%s", sidePrefix, partPrefix, baseName);
}

string
jointNaming(
    const string    sidePrefix;
    const string    partPrefix;
    const string    baseName;
    const int       index
)
{
    return sprintf("%s_%s_%s_%i", sidePrefix, partPrefix, baseName, index);
}

int
getJointSelection(
    export int  jointIDs[]
)
{
    string jointsList   = chs(PVS_JOINT_SELECTION);

    if(jointsList == ""){
        jointIDs = {};
        return 0;
    }

    string jointListSplitted[] = re_split(" ", jointsList);

    for(int i=0; i<len(jointListSplitted); i++){
        append(jointIDs, atoi(jointListSplitted[i]));
    }

    return 1;
}

void
setJointNameAndColor(
    const int      jointIDs[];
    const vector   jointPostions[]
)
{
    float centerTreshold = 0.001;

    vector  colorMiddle     = chv(PCOLOR_MIDDLE);
    vector  colorLeft       = chv(PCOLOR_LEFT);
    vector  colorRight      = chv(PCOLOR_RIGHT);
    string  baseName        = chs(PNAMING_BASE);
    string  partName        = chs(PNAMING_PART);
    string  prefixMiddle    = chs(PNAMING_PREFIX_MIDDLE);
    string  prefixLeft      = chs(PNAMING_PREFIX_LEFT);
    string  prefixRight     = chs(PNAMING_PREFIX_RIGHT);

    vector  pos, color;
    string  prefixSide, jointName;

    for(int i=0; i<len(jointIDs); i++){
        pos = jointPostions[i];
        if(pos.x <= -centerTreshold){
            color = colorRight;
            prefixSide = prefixRight;
        }else if(pos.x >= centerTreshold){
            color = colorLeft;
            prefixSide = prefixLeft;
        }else{
            color = colorMiddle;
            prefixSide = prefixMiddle;
        }
        if(partName == ""){
            jointName = jointNaming(prefixSide, baseName, jointIDs[i]);
        }else{
            jointName = jointNaming(prefixSide, partName, baseName, jointIDs[i]);
        }

        setpointattrib(GEO_SKELETON, ATTRIB_NAME, jointIDs[i], jointName);
        setpointattrib(GEO_SKELETON, "Cd", jointIDs[i], color);
    }    
}

void
setJointColor(
    const int      jointIDs[];
    const vector   jointPostions[]
)
{
    float centerTreshold = 0.001;

    vector colorMiddle  = chv(PCOLOR_MIDDLE);
    vector colorLeft    = chv(PCOLOR_LEFT);
    vector colorRight   = chv(PCOLOR_RIGHT);

    vector pos, color;

    for(int i=0; i<len(jointIDs); i++){
        pos = jointPostions[i];
        if(pos.x <= -centerTreshold){
            color = colorRight;
        }else if(pos.x >= centerTreshold){
            color = colorLeft;
        }else{
            color = colorMiddle;
        }
        setpointattrib(GEO_SKELETON, "Cd", jointIDs[i], color);
    }
}

void
setJointName(
    const int      jointIDs[];
    const vector   jointPostions[]
)
{
    // Get the joint position to find the side with the position x.
    float   centerTreshold = 0.001;

    string  baseName        = chs(PNAMING_BASE);
    string  partName        = chs(PNAMING_PART);
    string  prefixMiddle    = chs(PNAMING_PREFIX_MIDDLE);
    string  prefixLeft      = chs(PNAMING_PREFIX_LEFT);
    string  prefixRight     = chs(PNAMING_PREFIX_RIGHT);

    vector  pos;
    string  prefixSide, jointName;

    for(int i=0; i<len(jointIDs); i++){
        pos = jointPostions[i];
        if(pos.x <= -centerTreshold){
            prefixSide = prefixRight;
        }else if(pos.x >= -centerTreshold){
            prefixSide = prefixLeft;
        }else{
            prefixSide = prefixMiddle;
        }

        if(partName == ""){
            jointName = jointNaming(prefixSide, baseName, jointIDs[i]);
        }else{
            jointName = jointNaming(prefixSide, partName, baseName, jointIDs[i]);
        }

        setpointattrib(GEO_SKELETON, ATTRIB_NAME, jointIDs[i], jointName);
    } 

}

int
parentJoint()
{
    int parentJointID   = chi(PVS_JOINT_PARENTID);
    int jointID         = chi(PVS_JOINT_ID);


    // Check the scenario that don't allow to parent the joints.
    if(parentJointID == -1){
        return 0;
    }

    setpointattrib(GEO_SKELETON, ATTRIB_HELPER, parentJointID, 1);

    if(jointID == -1){
        return 0;
    }

    if(parentJointID == jointID){
        return 0;
    }

    // Do the parenting.
    int oldParentJointID;
    int oldParentPrimID;
    getJointParent(GEO_SKELETON, jointID, oldParentJointID, oldParentPrimID);

    if(oldParentJointID != -1){
        removeprim(GEO_SKELETON, oldParentPrimID, 0);
    }
    addprim(GEO_SKELETON, "polyline", parentJointID, jointID);

    return 1;
}

int
unParentJoint()
{
    int jointPrimID     = chi(PVS_JOINT_PRIMID);

    if(jointPrimID == -1){
        return 0;
    }

    int primPoints[] = primpoints(GEO_SKELETON, jointPrimID);

    setpointattrib(GEO_SKELETON, ATTRIB_HELPER, primPoints[0], 1);

    removeprim(GEO_SKELETON, jointPrimID, 0);
    return 1;
}

void
removeJointSelection()
{
    int jointIDs[];
    int status = getJointSelection(jointIDs);

    if(status == 0){
        return;
    }

    for(int i=0; i<len(jointIDs); i++){

        removepoint(GEO_CONSTRUCTION, jointIDs[i], 1);

        int rootID = findRoot(GEO_SKELETON, jointIDs[i], jointIDs);
        
        if(rootID == -1){
            continue;
        }

        int children[];
        int childrenPrims[];
        getJointChildren(GEO_SKELETON, jointIDs[i], children, childrenPrims);

        if(len(children) == 0){
            continue;
        }

        for(int j=0; j<len(children); j++){
            
            int inSelection = jointExist(children[i], jointIDs);
            if(inSelection == 0){
                addprim(GEO_SKELETON, "polyline", rootID, children[j]);
            }
        }
    }

}

int
removeJoint()
{

    int jointID     = chi(PVS_JOINT_ID);

    if(jointID == -1){
        return 0;
    }

    int jointPrims[] = pointprims(GEO_SKELETON, jointID);

    if(len(jointPrims) == 0){
        removepoint(GEO_SKELETON, jointID, 1);
        return 0;
    }

    int parentID = -1;
    int childrenIDs[];

    for(int i=0; i<len(jointPrims); i++){
        int points[] = primpoints(GEO_SKELETON, jointPrims[i]);

        if(points[0] == jointID){
            append(childrenIDs, points[1]);
        }else{
            parentID = points[0];
        }

        removeprim(GEO_SKELETON, jointPrims[i], 0);
    }

    removepoint(GEO_SKELETON, jointID, 1);

    if(parentID == -1){
        return 1;
    }

    for(int i=0; i<len(childrenIDs); i++){
        addprim(GEO_SKELETON, "polyline", parentID, childrenIDs[i]);
    }

    return 1;

}

int
insertJoint(
    export int      jointIDs[];
    export vector   jointPositions[]
)
{

    int     jointPrimID     = chi(PVS_JOINT_PRIMID);

    // If no prim ID, exit.
    if(jointPrimID == -1){
        return 0;
    }

    vector  jointPrimUVW    = chv(PVS_JOINT_PRIMUVW);
    int     insertType      = chi(PINSERT_TYPE);
    float   snapLocation    = chf(PINSERT_LOCATION);
    int     multiCount      = chi(PINSERT_MULTI_COUNT);


    // Define the primitive location.
    vector primUV = set(jointPrimUVW.x, jointPrimUVW.y, jointPrimUVW.z);
    
    // If type is snapped, use the snap location.
    if(insertType == 1){
        primUV.x = snapLocation;
    }

    // Get the current joint primitive points.
    int jointPrimPoints[] = primpoints(GEO_SKELETON, jointPrimID);
    // Delete the old connection.
    removeprim(GEO_SKELETON, jointPrimID, 0);

    // Behavior for type free and snapped.
    if(insertType == 0 || insertType == 1){

        // Get the new joint position.
        vector insertPos    = primuv(GEO_SKELETON, "P", jointPrimID, primUV);
        // Add the new joint.
        int     insertID    = addpoint(GEO_SKELETON, insertPos);
        // Connect the new joint with parent and child joints.
        int     parentPrim  = addprim(GEO_SKELETON, "polyline", jointPrimPoints[0], insertID);
        int     childPrim   = addprim(GEO_SKELETON, "polyline", insertID, jointPrimPoints[-1]);

        // New joint tag.
        setpointattrib(GEO_SKELETON, ATTRIB_HELPER, insertID, 1);

        // Update out joint list IDs.
        append(jointIDs, insertID);
        append(jointPositions, insertPos);

        return 1;
    }

    // Behavior for multi.
    if(insertType == 2){

        // Store the parent joint of the previous hierarchy.
        int previousJointID = jointPrimPoints[0];
        // Compute the distribution step.
        float uStep          = 1.0 / float(multiCount+1);
        // Loop to insert joints.
        for(int i=0; i<multiCount; i++){
            // Compute the current joint location.
            primUV.x            = uStep * float(i + 1);
            // Get the current joint position.
            vector  insertPos   = primuv(GEO_SKELETON, "P", jointPrimID, primUV);
            // Add the new joint.
            int     insertID    = addpoint(GEO_SKELETON, insertPos);
            // Connect the joint to previous parent.
            int     parentPrim  = addprim(GEO_SKELETON, "polyline", previousJointID, insertID);
            // If last joint, connect to the child.
            if(i == multiCount - 1){
                int childPrim = addprim(GEO_SKELETON, "polyline", insertID, jointPrimPoints[-1]);
            }
            // New joint tag.
            setpointattrib(GEO_SKELETON, ATTRIB_HELPER, insertID, 1);
            // Update out joint list IDs.
            append(jointIDs, insertID);
            append(jointPositions, insertPos);
            // Update the previous joint ID.
            previousJointID = insertID;
        }

        return 1;
    }

    return 0;
}

int
moveJoint(
    export int      jointIDs[];
    export vector   jointPostions[]
)
{
    // Get UI datas.
    int     jointID             = chi(PVS_JOINT_ID);
    int     projectionType      = chi(PPROJECTION_TYPE);
    float   surfaceDepthMix     = chf(PPROJECTION_SURFACEDEPTH_MIX);
    int     rayType             = chi(PPROJECTION_RAYTYPE);
    int     snapPoint           = chi(PPROJECTION_SNAPPOINT);
    int     depthType           = chi(PPROJECTION_DEPTHTYPE);
    vector  rayOrigin           = chv(PVS_RAY_ORIGIN);
    vector  rayDirection        = chv(PVS_RAY_DIRECTION); 
    int     surfacePointID      = chi(PVS_SKINPOINTID);

    if(jointID == -1){
        return 0;
    }

    // Get joint position.
    vector  jointPos;
    int status = projectionPosition(
            GEO_SKELETON,
            GEO_CONSTRUCTION,
            GEO_SKIN,
            jointID,
            projectionType,
            surfaceDepthMix,
            rayOrigin,
            rayDirection,
            snapPoint,
            surfacePointID,
            rayType,
            depthType,
            jointPos
        );

    if(status == 0){
        return 0;
    }

    // Check if we need to move the current joint and the joint selection.
    int jointSelection[];
    status = getJointSelection(jointSelection);

    if(status == 1){
        
        vector currentJointPos = point(GEO_SKELETON, "P", jointID); 

        for(int i=0; i<len(jointSelection); i++){
            vector pos = point(GEO_SKELETON, "P", jointSelection[i]);
            vector localPos = pos - currentJointPos;

            pos = jointPos + localPos;

            setpointattrib(GEO_SKELETON, "P", jointSelection[i], pos);
            append(jointIDs, jointSelection[i]);
            append(jointPostions, pos);
        }
    }

    setpointattrib(GEO_SKELETON, "P", jointID, jointPos);

    append(jointIDs, jointID);
    append(jointPostions, jointPos);

    return 1;
}

int
addJoint(
    export int      jointIDs[];
    export vector   jointPostions[]
)
{
    // Get UI datas.
    int     parentJointID       = chi(PVS_JOINT_PARENTID);
    int     projectionType      = chi(PPROJECTION_TYPE);
    float   surfaceDepthMix     = chf(PPROJECTION_SURFACEDEPTH_MIX);
    int     rayType             = chi(PPROJECTION_RAYTYPE);
    int     snapPoint           = chi(PPROJECTION_SNAPPOINT);
    int     depthType           = chi(PPROJECTION_DEPTHTYPE);
    vector  rayOrigin           = chv(PVS_RAY_ORIGIN);
    vector  rayDirection        = chv(PVS_RAY_DIRECTION);
    int     surfacePointID      = chi(PVS_SKINPOINTID);

    // Get joint position.
    vector  jointPos;
    int status = projectionPosition(
            GEO_SKELETON,
            GEO_CONSTRUCTION,
            GEO_SKIN,
            parentJointID,
            projectionType,
            surfaceDepthMix,
            rayOrigin,
            rayDirection,
            snapPoint,
            surfacePointID,
            rayType,
            depthType,
            jointPos
        );

    // Stop if status false.
    if(status == 0){
        return 0;
    }

    // Add the new joint.
    int     jointID     = addpoint(GEO_SKELETON, jointPos);

    // Add new joint tag.
    setpointattrib(GEO_SKELETON, ATTRIB_HELPER, jointID, 1);

    // Add to out joint list.
    append(jointIDs, jointID);
    append(jointPostions, jointPos);

    // Stop if no parent.
    if(parentJointID == -1){
        return 1;
    }

    // Connect the new joint with its parent.
    int jointPrimID = addprim(GEO_SKELETON, "polyline", parentJointID, jointID);

    return 1;
}

int
orientJoint()
{
    int jointID             = chi(PVS_JOINT_ID);

    if(jointID == -1){
        return 0;
    }

    setdetailattrib(GEO_SKELETON, "TEST", 1);

    vector  jointPos            = point(GEO_SKELETON, "P", jointID);
    matrix3 jointTransform      = point(GEO_SKELETON, "transform", jointID);
    int     jointMainAxis       = point(GEO_SKELETON, "orienMainAxis", jointID);
    int     jointSecAxis        = point(GEO_SKELETON, "orientSecondaryAxis", jointID);

    int orientTargetJoint   = chi(PVS_ORIENT_TARGETJOINTID);
    int orientTargetAxis    = chi(PVS_ORIENT_TARGETAXIS);
    int orientJointID       = chi(PVS_ORIENT_JOINTID);
    int orientAxis          = chi(PVS_ORIENT_AXIS);
    int skinPointID         = chi(PVS_SKINPOINTHIGHLIGHT);
    int lockAxis            = chi(PORIENT_LOCKAXIS);

    vector  targetJointPos;
    if(orientJointID > -1){
        targetJointPos      = point(GEO_SKELETON, "P", orientJointID);
    }else if(orientTargetJoint > -1){
        matrix3 targetTransform     = point(GEO_SKELETON, "transform", orientTargetJoint);
        vector  axis                = getAxis(orientTargetAxis, targetTransform);
        targetJointPos              = axis + jointPos;

    }else if(skinPointID > -1){
        targetJointPos              = point(GEO_SKIN, "P", skinPointID);
    }else{
        
        vector rayOrigin        = chv(PVS_RAY_ORIGIN);
        vector rayDirection     = chv(PVS_RAY_DIRECTION);

        int status = projectionFree(
            GEO_SKELETON, 
            jointID, 
            rayOrigin, 
            rayDirection, 
            targetJointPos);

        if(status == 0){
            return 0;
        }
    }
    
    jointOrient(
        jointPos,
        targetJointPos,
        orientAxis,
        0,
        jointMainAxis,
        jointSecAxis,
        lockAxis-1,
        jointTransform
    );

    setpointattrib(GEO_SKELETON, "transform", jointID, jointTransform);

    return 1;
}

void
setSekeletonColor()
{
    int     tool            = chi(PTOOL);

    vector  colorSelected   = chv(PCOLOR_SELECTED);
    vector  colorHighlight  = chv(PCOLOR_HIGHLIGHT);
    vector  colorHelper     = chv(PCOLOR_HELPER);
    vector  colorDisable    = chv(PCOLOR_DISABLE);

    string  jointSelection  = chs(PVS_JOINT_SELECTION);

    if(jointSelection != ""){
        string selection[]      = re_split(" ", jointSelection);
        for(int i=0; i<len(selection); i++){
            setpointattrib(geoself(), "selected", atoi(selection[i]), 1);
        }
    }

    int     jointHighligth  = chi(PVS_JOINT_HIGHLIGHT);
    if(jointHighligth > -1){
        setpointattrib(geoself(), "highlight", jointHighligth, 1);
    }

}

void
setJointIdentityTransform(
    const int   jointIDs[]
)
{
    matrix3 transform = ident();

    for(int i=0; i<len(jointIDs); i++){
        setpointattrib(GEO_SKELETON, "transform", jointIDs[i], transform);
    }
}

void
setJointDisableAttrib(
    const int jointIDs[]
)
{
    for(int i=0; i<len(jointIDs); i++){
        setpointattrib(GEO_SKELETON, "disable", jointIDs[i], 0);
    }    
}

void
jointTool()
{
    
    int     tool                        = chi(PTOOL);
    int     toolState                   = chi(PVS_TOOL_STATE);

    int     live                        = chi(PVS_LIVE);

    if(live == 1){
        toolState = 1;
    }

    if(toolState == 0){
        return;
    }

    int     toolStatus;
    int     jointIDs[];
    vector  jointPositions[];
    if(tool == TOOL_ADD_JOINT){
        toolStatus = addJoint(jointIDs, jointPositions);
        if(toolStatus == 1){
            setJointNameAndColor(jointIDs, jointPositions);
            setJointIdentityTransform(jointIDs);
            setJointDisableAttrib(jointIDs);
        }
        return;
    }

    if(tool == TOOL_MOVE_JOINT){
        toolStatus = moveJoint(jointIDs, jointPositions);
        if(toolStatus == 1){
            setJointColor(jointIDs, jointPositions);
        }
        return;
    }

    if(tool == TOOL_INSERT_JOINT){
        toolStatus = insertJoint(jointIDs, jointPositions);
        if(toolStatus == 1){
            setJointNameAndColor(jointIDs, jointPositions);
            setJointIdentityTransform(jointIDs);
            setJointDisableAttrib(jointIDs);
        }
        return;
    }

    if(tool == TOOL_REMOVE_JOINT){
        toolStatus = removeJoint();
        return;
    }

    if(tool == TOOL_PARENT_JOINT){
        toolStatus = parentJoint();
        return;
    }

    if(tool == TOOL_UNPARENT_JOINT){
        toolStatus = unParentJoint();
        return;
    }

    if(tool == TOOL_ORIENT_JOINT){
        toolStatus = orientJoint();
        return;
    }



}








#endif