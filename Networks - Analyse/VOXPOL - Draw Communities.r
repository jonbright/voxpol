###VOXPOL Network tools
#Auth: Jonathan Bright. Last update Feb 2017
##This file shows an example of using the generated layout data to make a network graphic in ggplot

#auto community positions
commpos <- read.csv("VOXPOL - Community Dataset - for visualisation.csv", sep=",")

#names
cnames <- read.csv("VOXPOL - Cluster Names.csv")
commpos <- merge(commpos, cnames, by.x = "community_id", by.y="community_id")

#inter community edges
cedges_auto <- read.csv("VOXPOL - Community-Edge Dataset - for visualisation.csv", sep=",")

library(ggplot2)
library(stringr)

commpos$label <- str_wrap(commpos$term, width=100)#label wrap

c <- ggplot() 
		+ geom_curve(data=cedges_auto, aes(x = sx, y = sy, xend = tx, yend = ty, alpha=weight), curvature = 0.15, arrow=arrow(type="closed", angle=10)) #edges
		+ geom_point(data=commpos, aes(x=x, y=y, size=community_size, colour=community_id)) #nodes 
		+ geom_text(data=commpos, aes(x=x, y=y, label=label)) # labels 
		+ theme_bw() + theme(line = element_blank(), axis.text=element_blank(), axis.title=element_blank()) + scale_alpha_continuous(guide=FALSE) + scale_size_continuous(name="Community\nSize", breaks=c(10, 50, 100, 200))#styling
c

ggsave("Community Network Diagram.svg", w=10, h=8)



