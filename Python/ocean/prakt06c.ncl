; prakt06c.ncl
;----------------------------------------------------------
; Plot advection results
;----------------------------------------------------------

;load necessary modules
;----------------------------------------------------------
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"
;----------------------------------------------------------

begin


;-- Read initial data from text file --

;infile = "./p06a_output.txt"  ;"./adv_in.txt"
infile = "./p06c_input.txt"  ;"./adv_in.txt"

u=-2. ;-2.
v=1.  ;must be positive
dx=0.1
dy=dx
dt=0.02

nx=144
ny=130
nt=90
var=new((/ny,nx,nt/),float)
varlast=new((/ny,nx/),float)

temp = asciiread(infile,(/nx,ny/),"float")   ;ncols,nrows
printVarSummary(temp)


;-- Implement methods for solving 2D advection equation --

var(:,:,0)=transpose(temp)
printVarSummary(var)

;--try the following variation in the position of the initial signal
shx=30
shy=30
var_temp=var*0.0
printVarSummary(var_temp)
var_temp(0:ny-shy-1,0:nx-shx-1,0)=var(shy:ny-1,shx:nx-1,0)
var_temp(shy:ny-1,shx:nx-1,0)=var(0:ny-shy-1,0:nx-shx-1,0)
var=var_temp


if (u .GE. 0.) then
;~~~~~~~~~~~~~~~~~~~~~~
 do ti=1,nt-1 
  varlast(:,:)=var(:,:,ti-1)
  do i=1,nx-1
   do j=1,ny-1
    var(j,i,ti) = varlast(j,i)-v*dt*(varlast(j,i)- varlast(j-1,i))/dy-u*dt*(varlast(j,i)-varlast(j,i-1))/dx
   end do
  end do
  ;-- boundaries
  var(:,0,ti) = 0 ;varlast(:,0)
  var(0,:,ti) = 0 ;varlast(0,:)
  var(:,nx-1,ti) = 0 ;varlast(:,nx-1)
  var(ny-1,:,ti) = 0 ;varlast(ny-1,:)  ;check this
 end do

else ;~~~~~~~~~~~~~~~~~~~~~~
 do ti=1,nt-1 
  varlast(:,:)=var(:,:,ti-1)
  do i=0,nx-2
   do j=1,ny-1
    var(j,i,ti) = varlast(j,i)-v*dt*(varlast(j,i)- varlast(j-1,i))/dy-u*dt*(varlast(j,i+1)-varlast(j,i))/dx
   end do
  end do
  ;-- boundaries
 var(0,:,ti) = 0 ;varlast(0,:)
 var(:,nx-1,ti) = 0 ;varlast(:,nx-1)

 end do

;~~~~~~~~~~~~~~~~~~~~~~
end if 


;-- Plot --

;******************************************************
;Create plot settings
;******************************************************


levels=(/ 0.0001,0.001,0.01,0.1,1,10,100,1000 /)  /100000.

;-- general --
res          = True
 res@gsnDraw              = False              ; don't draw
 res@gsnFrame             = False              ; don't advance frame

;-- map --
resT=res
 resT@pmLabelBarSide = "Right"
 resT@pmLabelBarParallelPosF = 0.5
 resT@pmLabelBarOrthogonalPosF = 0.28

 resT@lbOrientation = "Vertical"
 resT@lbTitleFont = "helvetica"

 resT@gsnSpreadColors = True     ; use full range of colors
 resT@cnFillOn = True            ; turn on color
 resT@cnLinesOn       = False    ; don't plot line countours
 resT@cnLevelSelectionMode =  "ExplicitLevels" 
 resT@cnLevels    = levels

;-- panel --
resF = True
 resF@gsnPaperMargin = 0.8


do ti=0,nt-1

 wks = gsn_open_wks("png","prakt06c"+sprinti("%02i",ti))
 gsn_define_colormap(wks,"amwg")          ; choose colormap  GMT_drywet  amwg
 plot = new(1,graphic)

 plot = gsn_csm_contour(wks,var(:,:,ti),resT)

 gsn_panel(wks,plot,(/1,1/),0)    ; draw everything

end do

;---Convert PNG images to animated GIF
;    cmd = "convert -delay 25 prakt06c*.png prakt06c_movie.gif"
;    system(cmd)
; --> Das Konvertieren dauert ja ewig. Kann man das nicht beschleunigen?

end
