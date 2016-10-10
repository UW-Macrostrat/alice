library("RPostgreSQL")

# Load driver and connection parameters
Driver<-dbDriver("PostgreSQL") # Establish database driver
Alice<-dbConnect(Driver, dbname = "alice", host = "localhost", port = 5432, user = "zaffos")

# Query the data
plateVelocity<-function(Connection=Alice) {
  FinalList<-vector("list",length=)
  for (i in 0:549) {
      Query<-paste("SELECT ",i+1," AS year1,",i," AS year2, a.plateid, ST_Distance_Spheroid(ST_Centroid(a.geom), ST_Centroid(b.geom), \'SPHEROID[\"WGS 84\",6378137,298.257223563]\') AS distance_m
      FROM merge.reconstructed_",i+1,"_merged AS a JOIN merge.reconstructed_",i,"_merged AS b ON a.plateid = b.plateid",sep="")
      FinalList[[i+1]]<-dbGetQuery(Connection,Query)
      }
   return(FinalList)
   }

# Bind the output togeter
PlateVelocity<-do.call(rbind,plateVelocity(Alice))

# Find mean and standard deviation
mean(PlateVelocity[,"distance_m"])/1000
sd(PlateVelocity[,"distance_m"])/1000
