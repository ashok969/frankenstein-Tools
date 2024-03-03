#ifndef __FRANKENSTEIN_SKELETON__
#define __FRANKENSTEIN_SKELETON__

#include <frankenstein_skeletonConstants.h>

void
getJointSelection(
    export int  jointIDs[]
)
{
    string jointList = chs(PVS_JOINT_SELECTION);
    string splitList[] = re_split(" ", jointList);
    resize(jointIDs, len(splitList));
    for(int i=0; i<len(splitList); i++){
        jointIDs[i] = atoi(splitList[i]);
    }
}


void
getJointParent(
    const int   geoID;
    const int   jointID;
    export int  parent;
    export int  parentPrim
)
{
    int prims[] = pointprims(geoID, jointID);

    parent = -1;

    for(int i=0; i<len(prims); i++){
        int points[] = primpoints(geoID, prims[i]);
        if(points[-1] == jointID){
            parent = points[0];
            parentPrim = prims[i];
            break;
        }
    }
}

void 
getJointChildren(
    const int   geoID;
    const int   jointID;
    export int  children[];
    export int  childrenPrims[]
)
{
    int prims[] = pointprims(geoID, jointID);

    for(int i=0; i<len(prims); i++){
        int points[] = primpoints(geoID, prims[i]);
        if(points[0] == jointID){
            append(children, points[-1]);
            append(childrenPrims, prims[i]);
        }
    }
}

int
jointExist(
    const int   jointID;
    const int   jointIDList[]
)
{
    for(int i=0; i<len(jointIDList); i++){
        if(jointID == jointIDList[i]){
            return 1;
        }
    }

    return 0;
}

int
findRoot(
    const int geoID;
    const int jointID;
    const int jointList[]
)
{
    int maxIter     = 1000;
    int iter        = 0;

    int rootID      = jointID;

    while(iter < maxIter){

        int parent;
        int parentPrim;
        getJointParent(geoID, rootID, parent, parentPrim);
        rootID = parent;

        if(rootID == -1){
            break;
        }

        int exist = jointExist(parent, jointList);

        if(exist == 0){
            break;
        }

        iter += 1;
    }

    return rootID;
}

int getLocalJointID(
    const int geoID;
    const int jointID
)
{
    int jointCount = npoints(geoID);
    
    for(int i=0; i<jointCount; i++){
        int localJointID = point(geoID, "jointID", i);
        if(localJointID == jointID){
            return i;
        }
    }
    
    return -1; 
}

vector getLocalJointPos(
    const int geoID;
    const int localJointID
)
{
    if(localJointID > -1){
        return point(geoID, "P", localJointID);
    }

    return {0.0, 0.0, 0.0};
}

matrix3 getLocalJointTransform(
    const int geoID;
    const int localJointID
)
{
    if(localJointID > -1){
        return point(geoID, "transform", localJointID);
    }

    return ident();
}


#endif