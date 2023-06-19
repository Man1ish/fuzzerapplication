/**
 * @params is a JSON object with optional fields "name" and "place".
 * @return a JSON object containing the message in a field called "msg".
 */

function hash(input) {
  let hash = 0;

  for (let i = 0; i < input.length; i++) {
    hash = (hash << 5) - hash + input.charCodeAt(i);
    hash &= hash;
  }

  return hash;
}


function main(params) {
  // log the parameters to stdout


  // if a value for name is provided, use it else use a default
  var input = "stranger"

  output = hash(input)


  // construct the message using the values for name and place
  // return {msg:  'Hello, ' + name + ' from ' + place + '!'};
  return {"result":output,'latency':1}
}