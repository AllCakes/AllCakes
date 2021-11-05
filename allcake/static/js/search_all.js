/*var sizeFilter = $('.size_filter input');
var targetList = $('.product li');

sizeFilter.click(function(){
    var targetValue = [];
    sizeFilter.filter(':checked').each(function(){
        targetValue.push('.'+$(this).val());
        //this 는 each의 value를 가져오는 것 => targetvalue에 저장
    });
    
    //=>배열에 담긴 것 확인용
    //동시에 두 사이즈 이상 가져오려면 배열에 ('.small, .medi') 같이 따옴표가 하나로 엮이고 콤마로 구분돼야함
    var targetClass=targetValue.join(', ');
    console.log(targetClass); 
    targetList.hide();
    $(targetClass).fadeIn( 2000 );
});
*/
/*
var $filter = $('.filter-group input');
var filters={}; //[]아니고 {} [],[] 둘다 합쳐야 하므로
var $output=$('.user-checked')
var $grid = $('.product').isotope({
    itemSelector: '.product li'
  });

$filter.click(function(){
    var $button=$(this);//클릭이벤트가 일어난 애를 this로
    var $buttonGroup = $button.parents('.div');
    var filterGroup = $buttonGroup.attr('data-filter-group');

    filters[ filterGroup ] = $button.val();

     // combine filters
    var filterValue = concatValues( filters );
      // console.log(filterValue);
  // set filter for Isotope
    $output.text( filterValue );
    $grid.isotope({ filter: filterValue });
   
});

// change is-checked class on buttons
$('.btn').each( function( i, buttonGroup ) {
  var $buttonGroup = $( buttonGroup );
  $buttonGroup.on( 'click', 'btn', function( event ) {
    $buttonGroup.find('.is-checked').removeClass('is-checked');
    var $button = $( event.currentTarget );
    $button.addClass('is-checked');
  });
});

function concatValues( obj ) {
    var value = '';
    for ( var prop in obj ) {
      value += obj[ prop ];
    }
    return value;
  }
  */

  var $container = $('.product').isotope({
    itemSelector: '.product li'
  });
  var $output = $('.user-checked');
  
  // filter with selects and checkboxes
  var $checkboxes = $('.filter-group input');
  
  $checkboxes.change( function() {
    // map input values to an array
    var inclusives = [];
    // inclusive filters from checkboxes
    $checkboxes.each( function( i, elem ) {
      // if checkbox, use value if checked
      if ( elem.checked ) {
        inclusives.push( elem.value );
      }
    });
  
    // combine inclusive filters
    var filterValue = inclusives.length ? inclusives.join(', ') : '*';
  
    $output.text( filterValue );
    $container.isotope({ filter: filterValue })
  });
  

// init Isotope
var $grid = $('.product').isotope({
  itemSelector: '.product li',
  //layoutMode: 'fitRows'
});
// filter functions
var filterFns = {
  // show if number is greater than 50
  onlystores: function() {
    var name = $(this).find('.typed').text();
    return name.match( "stores" );
  },
  // show if name ends with -ium
  onlycakes: function() {
    var name = $(this).find('.typed').text();
    return name.match( "cakes" );
  }
};
// bind filter on select change
$('.filters-select-type').on( 'change', function() {
  // get filter value from option value
  var filterValue = this.value;//*,stores,혹은 cakes 중에 하나 가져와
  // use filterFn if matches value
  filterValue = filterFns[ filterValue ] || filterValue;
  $grid.isotope({ filter: filterValue });
});

//노션이나~~줌새로파서 :D!! ><
//서버랑 통신.. => 배운 다으메 응용..
