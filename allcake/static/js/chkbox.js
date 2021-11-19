// templating
var colors = [ 'red', 'green', 'blue', 'orange' ];
var sizes = [ 'small', 'medium', 'large' ];
var prices = [ 10, 20, 30 ];

createItems();

// init Isotope
var $container = $('#container').isotope({
  itemSelector: '.item'
});

var $output = $('#output');

// filter with selects and checkboxes
var $checkboxes = $('#form-ui input');

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


function createItems() {

  var $items;
  // loop over colors, sizes, prices
  // create one item for each
  for (  var i=0; i < colors.length; i++ ) {
    for ( var j=0; j < sizes.length; j++ ) {
      for ( var k=0; k < prices.length; k++ ) {
        var color = colors[i];
        var size = sizes[j];
        var price = prices[k];
        var $item = $('<div />', {
          'class': 'item ' + color + ' ' + size + ' price' + price
        });
        $item.append( '<p>' + size + '</p><p>$' + price + '</p>');
        // add to items
        $items = $items ? $items.add( $item ) : $item;
      }
    } 
  }

  $items.appendTo( $('#container') );

}
