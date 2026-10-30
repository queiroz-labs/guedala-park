/* Regras de navegação móvel, independentes do DOM. */
;(function(root){
 function headerState(compact,{width,y,delta,searchFocused}){
  if(width>760||y<=24||searchFocused)return false;
  if(delta<0)return false;
  if(delta>0&&y>80)return true;
  return compact;
 }
 root.GuedalaMobileUX={headerState};
})(globalThis);
