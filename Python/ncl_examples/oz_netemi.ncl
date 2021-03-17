load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/wrf/WRFUserARW.ncl"

begin
;
; The WRF ARW input file.  
; This needs to have a ".nc" appended, so just do it.

  a = addfile("/work/nkuech/wrf/wrfout_d01_2009-09-21_00:00:00_S04.nc","r")
;  print(a)

;  We generate plots, but what kind do we prefer?

;   type = "x11"
  type = "pdf"
;  type = "ps"
;  type = "ncgm"

; Set some Basic Plot options
    ARWres = True
;    ARWres@MainTitle     = times(time)     
;    ARWres@vpWidthF      = .6           ; Overwrite basic plot size
;    ARWres@vpHeightF     = .3

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;  What times and how many time steps are in the data set?

  times  = wrf_user_list_times(a)  ; get times in the file
  ntimes = dimsizes(times)         ; number of times in the file

; This is the big loop over all of the time periods to process.

   do time = 4,ntimes-1,4

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
; First get the variables we will need        
    
  ter = wrf_user_getvar(a,"HGT_M",0)
  ddep5 = wrf_user_getvar(a,"DRYDEP_5",time)
  net5a = wrf_user_getvar(a,"EDUST5",time)
  net5  = net5a(0,:,:) + ddep5(:,:)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

net5@units = "ug/m2/s"
delete(net5@units)		;delete attribute that it does not appear as UnitLabel

;----------------------------------------------------------
wks = gsn_open_wks(type,"oz_netemi_"+times(time))
;-------

ARWres@cnFillOn			= True
ARWres@cnLevelSelectionMode = "ExplicitLevels"
ARWres@cnLevels = (/1.,2.,3.,5.,10.,20.,30.,50.,100.,200.,300.,500/)
;ARWres@ContourParameters	= (/ -50.0, 0.0, 1.0 /)

gsn_define_colormap(wks, "WhiteBlueGreenYellowRed")

ARWres@lbBoxLinesOn		= False
;ARWres@lbLabelStride		= 20
ARWres@lbTitleOn		= True
ARWres@lbTitleString		="total dust dep [ug/m2/s]"
;ARWres@NoHeaderFooter     	= True            ; Ste footers off
ARWres@FieldTitle 		= times(time)	
ARWres@ValidTime		= False	
ARWres@MainTitle		= " "
ARWres@InitTime			= False
ARWres@Footer			= False

net = wrf_contour(a,wks,net5,ARWres)
;-------
mpres = True
mpres@mpGeophysicalLineThicknessF = 1.5
mpres@mpGeophysicalLineColor=1
mpres@mpGridMaskMode="MaskLand"
mpres@mpGridLineColor="grey80"

pltres = True

plot = wrf_map_overlays(a,wks,net,pltres, mpres)
delete(wks)
;----------------------------------------------------------

;    end do

;  ************************************************************

  end do  ;       end of the time loop

end

;.gif animation erstellen:
;convert -delay 50 -dispose 2 -loop 0 *.ps SandstormAUS.gif