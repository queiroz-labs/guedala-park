/* Regras de navegação móvel, independentes do DOM. */
;(function(root){
 function headerState(compact,{width,y,delta,searchFocused}){
  if(y<=24||searchFocused)return false;
  if(delta<0)return false;
  if(delta>0&&y>80)return true;
  return compact;
 }
 function tabScroll({left,right,viewLeft,viewRight,scrollLeft}){
  if(left<viewLeft+24)return Math.max(0,scrollLeft+left-viewLeft-24);
  if(right>viewRight-24)return Math.max(0,scrollLeft+right-viewRight+24);
  return scrollLeft;
 }
 const tabEdges=(left,width,total)=>({left:left>1,right:left+width<total-1});
 root.GuedalaMobileUX={headerState,tabScroll,tabEdges};
})(globalThis);
