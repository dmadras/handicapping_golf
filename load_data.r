drawplots <- function(dat, imgd){
  setwd(imgd)
  holelist = c('h1','h2', 'h3','h4','h5', 'h6','h7','h8','h9','h10','h11','h12','h13','h14','h15','h16','h17','h18')
  holes = subset(dat, select = holelist)
  mn = sapply(holes, mean)
  mn_diff = mn - pars
  
  png('means-pars.png')
  plot(pars, mn, xlab='Par', ylab='Mean score')#, main='Mean Score by Par Level')
  dev.off()
  
  png('mndiffs-pars.png')
  plot(pars, mn_diff, xlab='Par', ylab='Mean score above par')#, main='Mean Score above Par by Par Level' )
  dev.off()
  
  png('diff-mndiffs.png')
  plot(difficulty, mn_diff, xlab='Difficulty ranking', ylab='Mean score above par', col=gray(c(1,1,0.7, 0.5, 0))[pars], pch=15)#, main='Mean score above par by difficulty ranking')
  abline(mn_diff ~ difficulty)
  dev.off()
  
  png('diff-pars.png')
  plot(difficulty, pars, xlab='Difficulty ranking', ylab='Par')#, main='Par by difficulty ranking'
  dev.off()

  # heatmap(table(dat$h1, dat$h2), Rowv = NA, Colv = 'Rowv', scale='none', xlab='Score on Hole1', xlab='Score on Hole1')
  
  png('hdcp-dist.png')
  barplot(table(dat$hdcp), xlab='Handicap', ylab='Count')#, main='Distribution of Handicaps in Shaughnessy dataset'
  #hist(table(dat$hdcp), main='Distribution of Handicaps in Shaughnessy dataset', xlab='Handicap', ylab='Count')
  dev.off()
  
  png('diff-mndiff-bypar.png')
  par(mfrow=c(1,3))
  p=3
  plot(difficulty[pars==p], mn_diff[pars==p], xlab='Difficulty Rating', ylab='Mean score above par', ylim=c(0.6, 1.6))#, main=sprintf('Par %d', p)
  p=4
  plot(difficulty[pars==p], mn_diff[pars==p], xlab='Difficulty Rating', ylab='Mean score above par',ylim=c(0.6, 1.6))#, main=sprintf('Par %d', p)
  p=5
  plot(difficulty[pars==p], mn_diff[pars==p], xlab='Difficulty Rating', ylab='Mean score above par',ylim=c(0.6, 1.6))#, main=sprintf('Par %d', p)
  dev.off()
  
  par(mfrow=c(1,1))
  
  sds = sapply(holes, sd)

  png('sd-par.png')
  plot(pars, sds, xlab='Par', ylab='SD')#, main='Standard deviation by Par'
  dev.off()
  
  png('diff-sd.png')
  plot(difficulty, sds, xlab='Difficulty Ranking', ylab='SD')#, main='Standard Deviation by difficulty ranking'
  abline(sds ~ difficulty)
  dev.off()
  
  png('mndiff-sd.png')
  plot(mn_diff, sds, xlab='Diff to Mean', ylab='SD', col=gray((1:18)/25)[difficulty], pch=15)#, main='Standard deviation vs. mean score above par by player'
  abline(sds ~ mndiff)
  dev.off()
  
  hp = sweep(holes, 2, pars, `-`)
  hpmn <- apply(hp, 1, mean)
  hpmn3 = apply(hp[,pars == 3], 1, mean)
  hpmn4 = apply(hp[,pars == 4], 1, mean)
  hpmn5 = apply(hp[,pars == 5], 1, mean)
  hpsum <- apply(hp, 1, sum)
  hpsd <- apply(hp, 1, sd)
  hpsd3 = apply(hp[,pars == 3], 1, sd)
  hpsd4 = apply(hp[,pars == 4], 1, sd)
  hpsd5 = apply(hp[,pars == 5], 1, sd)
  sdrange = c(0, 3)
  mnrange = c(-1,3.5)
  
  png('sd-mn.png')
  plot(hpsd, hpmn,xlab='SD', ylab='Mean', col=gray((1:length(unique(dat$hdcp + 3)))/length(unique(dat$hdcp + 3)))[dat$hdcp + 3], pch=15)#, main='Standard deviation vs. Mean score by player'
  dev.off()
  
  png('sd-mn-bypar.png')
  par(mfrow=c(1,3))
  plot(hpsd3, hpmn3, xlab='SD', ylab='Mean', xlim=sdrange, ylim=mnrange)
  plot(hpsd4, hpmn4, xlab='SD', ylab='Mean', xlim=sdrange, ylim=mnrange)
  plot(hpsd5, hpmn5, xlab='SD', ylab='Mean', xlim=sdrange, ylim=mnrange)
  dev.off()
  par(mfrow=c(1,1))
  
  png('hdcp-mn.png')
  plot(dat$hdcp, hpmn, xlab='Handicap', ylab='Average strokes above par')#, main='Player mean score above par by handicap'
  lines(lowess(dat$hdcp, hpmn), col='blue')
  dev.off()
  
  png('hdcp-mn-bypar.png')
  par(mfrow=c(1,3))
  plot(dat$hdcp, hpmn3, xlab='Handicap', ylab='Mean', ylim=mnrange)
  plot(dat$hdcp, hpmn4, xlab='Handicap', ylab='Mean', ylim=mnrange)
  plot(dat$hdcp, hpmn5, xlab='Handicap', ylab='Mean', ylim=mnrange)
  dev.off()
  par(mfrow=c(1,1))
  
  png('hdcp-sd.png')
  plot(dat$hdcp, hpsd, xlab='Handicap', ylab='SD')#, main='Standard Deviation above par by player handicap'
  dev.off()
  png('hdcp-sd-bypar.png')
  par(mfrow=c(1,3))
  plot(dat$hdcp, hpsd3, xlab='Handicap', ylab='SD', ylim=sdrange)
  plot(dat$hdcp, hpsd4, xlab='Handicap', ylab='SD', ylim=sdrange)
  plot(dat$hdcp, hpsd5, xlab='Handicap', ylab='SD', ylim=sdrange)
  dev.off()
  par(mfrow=c(1,1))
  png('hdcp-adjttl.png')
  plot(dat$hdcp, dat$ttl - dat$hdcp, xlab='Handicap', ylab='Total strokes minus handicap')#, main='Adjusted total score by handicap'
  lines(lowess(dat$hdcp, dat$ttl - dat$hdcp), col='blue')
  dev.off()
  png('hdcp-ttl.png')
  plot(dat$hdcp, dat$ttl, xlab='Handicap', ylab='Total')#, main='Total score by handicap'
  dev.off()  
  
  p3 = apply(hp[which(pars==3)], 1, mean) - 3
  p4 = apply(hp[which(pars==4)], 1, mean) - 4
  p5 = apply(hp[which(pars==5)], 1, mean) - 5
  sink('lmsummaries.txt')
  print('model hdcp by par levels')
  print(summary(lm(dat$hdcp / 18 ~ p3 + p4 + p5)))
  print('model hdcp by holes')
  print(summary(lm(dat$hdcp ~ ., data=hp)))
  print('model sd by hdcp')
  print(summary(lm(hpsd~dat$hdcp)))
  print('model mn by hdcp')
  print(summary(lm(hpmn~dat$hdcp)))
  print('model mndiff by difficulty')
  print(summary(lm(mn_diff~difficulty)))
  print('model sds by difficulty')
  print(summary(lm(sds~difficulty)))
  print('model hpmn3 by hdcp')
  print(summary(lm(hpmn3~dat$hdcp)))
  print('model hpmn4 by hdcp')
  print(summary(lm(hpmn4~dat$hdcp)))
  print('model hpmn5 by hdcp')
  print(summary(lm(hpmn5~dat$hdcp)))
  print('model hpsd3 by hdcp')
  print(summary(lm(hpsd3~dat$hdcp)))
  print('model hpsd4 by hdcp')
  print(summary(lm(hpsd4~dat$hdcp)))
  print('model hpsd5 by hdcp')
  print(summary(lm(hpsd5~dat$hdcp)))
  sink()


}

datadir='/Users/madras/Documents/tim - golf/data/csv'
setwd(datadir)

pars = c(5,4,3,4,5,4,5,3,4,4,5,3,4,4,5,4,3,4)
difficulty = c(9,5,17,1,11,15,3,13,7,4,10,16,2,14,6,12,18,8)
BIG = 10000

weeks = as.character(c(1, 6, 12, 17))
doall = length(weeks) == 4
doallonly = FALSE & doall
if (doall){
  bigdat = NULL
}

for (wk in weeks) {
  imgdir=sprintf('/Users/madras/Documents/tim - golf/figs/wk%s', wk)
  hdcpfile = sprintf('Week #%s - Handicaps.csv', wk)
  scorefile = sprintf('Week #%s - Scores.csv', wk)
  
cn = c('x0', "Hole", "name1", 'x1', 'x2', 'hdcp1', 'x3', 'name2', 'hdcp2', 'x4', 'name3', 'x5', 'hdcp3','x8', 'name4', 'x6', 'x7', 'hdcp4', 'x', 'x', 'x')
d = read.csv(hdcpfile, fill = TRUE, col.names = cn, header = FALSE)
d = d[c("Hole", "name1", 'hdcp1',  'name2', 'hdcp2', 'name3', 'hdcp3', 'name4','hdcp4')]
d = subset(d, name1 != '')
di = d
x = (unlist(c(unname(d['name1']), unname(d['name2']), unname(d['name3']), unname(d['name4']))))
y = (unlist(c(unname(d['hdcp1']), unname(d['hdcp2']), unname(d['hdcp3']), unname(d['hdcp4']))))
#y = y + BIG

hc2 = data.frame(name = x, hdcp = as.numeric(as.character(y)))
hc = hc2
levels(hc$hdcp) = c(levels(hc$hdcp), 0)
hc$hdcp[grepl('NH',hc$hdcp)] <- 0


h = subset(hc, hc$hdcp != 'NA')


cn = c('pos', 'hole', 'name', 'x6', 'x5', 'h1', 'h2', 'h3','h4', 'h5', 'h6', 'h7','h8','h9','x4','out', 'x3','h10','h11','h12','h13', 'h14', 'h15', 'h16', 'h17', 'h18','x3','inscore','x1', 'ttl', 'x7','x8','x9','x10')
d = read.csv(scorefile, fill = TRUE, col.names = cn, header = FALSE)
d = subset(d, name != '' & name != 'Mystery Player' & name != 'Mystery' & 'ttl' != '' & 'out' != '')
d = d[c('pos', 'hole', 'name','h1','h2','h3','h4','h5', 'h6', 'h7','h8','h9','out', 'h10','h11','h12','h13','h14','h15','h16','h17','h18','inscore','ttl')]
d$h17 <- droplevels(d$h17)
d$h17 <- as.numeric(levels(d$h17))[d$h17]
d$ttl <- as.numeric(levels(d$ttl))[d$ttl]

dat = merge(h, d, by=c('name'))
if (doall) {
  if (is.null(bigdat)) {
    bigdat = dat
  } else {
    bigdat = rbind(bigdat, dat)
  }
}

if (!doallonly){
  currd = getwd()
  drawplots(dat, imgdir)
  setwd(currd)
}
}

if (doall) {
  currd = getwd()
  all_imgdir = sprintf('/Users/madras/Documents/tim - golf/figs/wk%s', 'all')
  drawplots(bigdat, all_imgdir)
  setwd(currd)
}
write.csv(bigdat, file = "golfdata.csv",row.names=FALSE)