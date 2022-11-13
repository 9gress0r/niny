#[path = "./lexer.rs"] mod lexer;
use lexer::{ContentType, Tokenizer, Token, Tokens};

enum Types {
    Int(i32),
    Float(f32),
    String(String),
    Bool(bool),
    Char(char),
}

// IR for the generated code
enum Commands {
    Push(Types),
    Pop,
    Add,
    Sub,
    Mul,
    Div,
    Mod,
    Dump
}

struct Generator {
    tokens: Vec<Token>,
    commands: Vec<Commands>,
    caret: usize,
}

impl Generator {
  pub fn new() -> Self {
    Generator {
      tokens: Vec::new(),
      commands: Vec::new(),
      caret: 0,
    }
  }

  pub fn next(&mut self) -> Option<Token> {
    if self.caret >= self.tokens.len() {
      return None
    }

    let token = self.tokens[self.caret].clone();
    self.caret += 1;
    return Some(token)
  }

  pub fn peek(&self) -> Option<Token> {
    if self.caret >= self.tokens.len() {
      return None
    }

    return Some(self.tokens[self.caret].clone())
  }

  fn generate_from_string(&mut self, content: String) {
    let mut tokenizer = Tokenizer::new(ContentType::String(content));
    tokenizer.tokenize();
    self.tokens = tokenizer.stream;

    loop {
      let token = self.next();

      if token.is_none() {
        break
      }

      if token.as_ref().unwrap().kind == Tokens::Identifier {
        match token.unwrap().content.as_str() {
          "push" => {
            let arg = self.next();

            if arg.is_none() {
              panic!("Expected argument for push")
            }

            let arg = arg.unwrap();

            use Tokens::*;
            match arg.kind {
              IntegerLiteral => {
                self.commands.push(Commands::Push(Types::Int(arg.content.parse::<i32>().unwrap())));
              },
              FloatLiteral => {
                self.commands.push(Commands::Push(Types::Float(arg.content.parse::<f32>().unwrap())));
              },
              StringLiteral => {
                self.commands.push(Commands::Push(Types::String(arg.content)));
              },
              CharLiteral => {
                self.commands.push(Commands::Push(Types::Char(arg.content.chars().nth(0).unwrap())));
              },
              _ => {
                panic!("Invalid argument for push");
              }
            }
          },

          "pop" => {
            self.commands.push(Commands::Pop);
          },

          "add" => {
            self.commands.push(Commands::Add);
          },

          "sub" => {
            self.commands.push(Commands::Sub);
          },

          "mul" => {
            self.commands.push(Commands::Mul);
          },

          "div" => {
            self.commands.push(Commands::Div);
          },

          "mod" => {
            self.commands.push(Commands::Mod);
          },

          "dump" => {
            self.commands.push(Commands::Dump);
          },

          _ => {
            panic!("Invalid command");
          }
        }
      }
    }
  }
}
