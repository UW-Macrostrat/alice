library("rgdal")

# A simple loop to cull out all sedimentary rock polygons of age i
# Will write all files to your current working directory as a GeoJson
cullBurwell<-function(Shapefile) {
    for (i in 1:550) {
 	    Temp<-tryCatch(
 		    subset(Shapefile,Shapefile$LITH=="sedimentary rocks" & Shapefile$AGE_BOTTOM>=i & Shapefile$AGE_TOP<=i),
 		    error=function(Error) return(NA)
 		    )
 	    if (class(Temp)!="SpatialPolygonsDataFrame") {
 	        print(i);
 	        next;
 	        }
 	    writeOGR(Temp,paste("Sedimentary","Age",i,sep="_"),layer="Temp",driver="GeoJSON")
 	    }
    }
