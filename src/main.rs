mod tokens;

fn main() {
  let content = String::from("macro print do");
  let tokenizer = tokens::Tokenizer::new(content);

  for token in tokenizer.tokenize() {
    println!("{}", token);
  }
}
