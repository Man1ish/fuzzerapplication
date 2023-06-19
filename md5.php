function hash($input) {
  $hash = 0;

  for ($i = 0; $i < strlen($input); $i++) {
    $hash = ($hash << 5) - $hash + ord($input[$i]);
    $hash &= $hash;
  }

  return $hash;
}

function main(array $params) : array {
  // if a value for name is provided, use it else use a default
  $input = isset($params['name']) ? $params['name'] : 'stranger';

  $output = hash($input);

  // construct the message using the values for name and place
  return [
    'result' => $output,
    'latency' => 1
  ];
}
