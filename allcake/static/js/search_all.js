 //////체크박스 포함//////////////////
 var $container = $('.grid').isotope({
    itemSelector: '.product li'
  });
  var $output = $('.user-checked');

  // filter with selects and checkboxes
  var $checkboxes = $('.filter-group input');//체크박스
  $checkboxes.change( function() {//체크박스가 바뀌면 function 실행
    // map input values to an array
    var inclusives = [];
    // inclusive filters from checkboxes
    $checkboxes.each( function( i, elem ) {
      // if checkbox, use value if checked
      if ( elem.checked ) {
        inclusives.push( elem.value );//사용자가 체크한 값을 넣어주기
      }
    });
    // combine inclusive filters
    var filterValue = inclusives.length ? inclusives.join(', ') : '*';
    $output.text( filterValue );//이용자가 체크한 값 무엇인지 알려주는 텍스트 
    $container.isotope({ filter: filterValue })

  });
  
////////////////////여기서부턴 케이크집만/ 케이크만, 토글바//////////////////////
/*
var $grid = $('.grid').isotope({
  itemSelector: '.product'
});
// filter functions
var filterFns = {
  // show if number is greater than 50
  onlystores: function() {
    var name1 = $(this).find('.typed').text();
    return name1.match( /stores$/ );
  },
  // show if name ends with -ium
  onlycakes: function() {
    var name2 = $(this).find('.typed').text();
    return name2.match( /cakes$/ );
  }
};

$('.filters-select-type').on( 'change', function() {
  // get filter value from option value
  var filterValue2 = this.value;//*,stores,혹은 cakes 중에 하나 가져와
  // use filterFn if matches value
  filterValue2 = filterFns[ filterValue2 ] || filterValue2;
  $grid.isotope({ filter: filterValue2 });
});
*/

