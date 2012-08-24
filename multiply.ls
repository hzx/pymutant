
class World {
  1. int X;  // "1. " servers the same purpose as "= 1"
  2. int Y;  // does in Google protocol buffer syntax.
};

return fn(world, browser, session) {
  var incr = fn(number) {
    number := number + 1;
  };

  return <code style={ fontSize: "16px" }>
    <div>
      'X: '
      <input data=world.X type="number" />
      <button onclick=(fn() incr(world.X))>'+1'</button>
    </div>
    <div>
      'Y: '
      <input data=world.Y type="number" />
      <button onclick=(fn() incr(world.Y))>'+1'</button>
    </div>
    <div style={ fontSize: '30px' }>
      '('
      <em> world.X </em>
      ' * '
      <em> world.Y </em>
      ' = '
      <strong> world.X * world.Y </strong>
      ')'
    </div>
  </code>;
};
