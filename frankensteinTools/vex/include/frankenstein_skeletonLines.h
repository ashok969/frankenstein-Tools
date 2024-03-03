#ifndef __FRANKENSTEIN_SKELETON_LINES__
#define __FRANKENSTEIN_SKELETON_LINES__

#include <frankenstein_skeletonConstants.h>

void
buildSkeletonLines(
    const int   sourceGeoID
)
{
    vector colorHelper = chv(PCOLOR_HELPER);

    int primCount = nprimitives(sourceGeoID);

    for(int i=0; i<primCount; i++){

        int points[] = primpoints(sourceGeoID, i);

        vector p0pos = point(sourceGeoID, "P", points[0]);
        vector p1pos = point(sourceGeoID, "P", points[-1]);

        vector color = point(sourceGeoID, "Cd", points[0]);

        vector primHelper = prim(sourceGeoID, "helper", i);
        if(primHelper == 1){
            color = colorHelper;
        }

        int p0 = addpoint(geoself(), p0pos);
        int p1 = addpoint(geoself(), p1pos);

        int primID = addprim(geoself(), "polyline", p0, p1);

        setpointattrib(geoself(), "Cd", p0, color);

    }

}



#endif