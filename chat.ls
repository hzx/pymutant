
class World {
  1. ChatMessage[] messages;
};

class ChatMessage {
  1. User user;
  2. string text;
};

return fn(world, browser, session) {
  // Style information omitted to improve readability.
  var renderMessage = fn(message) {
    var bubble_style = { ... };
    return <div>
      <img src=message.user.small_pic_url />
      <div style=bubble_style>
        <b message.user.name, ': ' </b>
        <div> message.text </div>
      </div>
    </div>;
  };
  var postMessage = fn() {
    messages += ChatMessage {
      user: session.user,
      text: session.new_comment
    };
    session.new_comment := '';
  };

  return <table>
    <tr><td>
      messages.map(renderMessage)
    </td></tr>
    <tr><td>
      <img src=(session.user.small_pic_url) />
      <div>
        <input data=session.user.name /> <b>' (your nickname) '</b>
        <form onsubmit=postMessage>
          <input data=session.new_comment hasFocus=true />
        </form>
      </div>
    </td></tr>
  </table>;
};
