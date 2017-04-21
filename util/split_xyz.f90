program convert
implicit none
integer::iat,nat,i,j,k,iframe,stat
real(8)::rxyz(3),c(9)
character(len=2)::atname
character(len=4)::fn
character(len=12)::filename
!open(1,file="cell")
iframe=0
do while (1==1)
read(*,*,IOSTAT=stat)nat 
!read(1,*,IOSTAT=stat) (c(i),i=1,9) 
IF(IS_IOSTAT_END(stat)) STOP
if (iframe<45) continue 
write(fn,'(I4.4)') iframe
filename='set.'//fn//'.xyz'
open(1,file=filename)
read(*,*) 
!read(*,*) 
write(1,*) nat 
write(1,*) "sphere cut out from bulk " !'Lattice="',(c(i),i=1,9), '" Properties=species:S:1:pos:R:3'
do iat=1,nat
  read(*,*) atname,(rxyz(i),i=1,3)
  write(1,'(1a,3(2X,F5.1))') atname,(rxyz(i),i=1,3)
enddo
close(1)
iframe=iframe+1
enddo
end program convert
