use std::fmt::{Display, Error, Formatter};
use std::io::{BufReader, BufRead};
use std::fs::File;

use regex::Regex;

macro_rules! pair {
  ($a:expr => $b:expr) => {
    Pair {
      first:  $a,
      second: $b
    }
  };
}

#[derive(Copy, Clone, Eq, PartialEq)]
pub enum Tokens {
  // Literals
  IntegerLiteral,
  FloatLiteral,
  StringLiteral,
  CharLiteral,

  Identifier,
  Operator,
  Separator,
  Keyword,
  Comment,
  EOL
}

impl Display for Tokens {
  fn fmt(
    &self,
    f: &mut Formatter
  ) -> Result<(), Error> {
    use Tokens::*;
    let token = match *self {
      IntegerLiteral => "IntegerLiteral",
      FloatLiteral => "FloatLiteral",
      StringLiteral => "StringLiteral",
      CharLiteral => "CharLiteral",
      Identifier => "Identifier",
      Operator => "Operator",
      Separator => "Separator",
      Keyword => "Keyword",
      Comment => "Comment",
      EOL => "EOL"
    };

    write!(f, "{}", token)
  }
}

#[derive(Copy, Clone)]
pub struct Pair<A, B> {
  pub first:  A,
  pub second: B
}

pub struct Token {
  pub kind:    Tokens,
  pub content: String,
  pub line:    usize,
  pub column:  usize
}

impl Display for Token {
  fn fmt(
    &self,
    f: &mut Formatter
  ) -> Result<(), Error> {
    write!(
      f,
      r"Token '{}' of type `{}`",
      self.content.replace("\n", "\\n"),
      self.kind
    )
  }
}

pub enum ContentType {
  File(String), // Path
  String(String)
}

pub struct Tokenizer {
  token_map: Vec<Pair<&'static str, Tokens>>,
  content:   ContentType,
  pub stream: Vec<Token>
}

impl Tokenizer {
  pub fn new(content: ContentType) -> Tokenizer {
    use Tokens::*;
    Tokenizer {
      content,
      stream: Vec::new(),
      token_map: vec![
        pair!(r"\$.*" => Comment),
        // Literals
        pair!(r#""[^"\\]*(\\.[^"\\]*)*""# => StringLiteral),
        pair!(r"'\.*'" => CharLiteral),
        pair!(r"[+-]?[0-9]+" => IntegerLiteral),
        pair!(r"[+-]?[0-9]+\.[0-9]*" => FloatLiteral),
        // Keywords
        pair!("if" => Keyword),
        pair!("else" => Keyword),
        pair!("macro" => Keyword),
        pair!("do" => Keyword),
        pair!("end" => Keyword),
        // Operators
        pair!(r"\+" => Operator),
        pair!(r"\-" => Operator),
        pair!(r"\*" => Operator),
        pair!(r"/" => Operator),
        // Separators
        pair!(r"\(" => Separator),
        pair!(r"\)" => Separator),
        pair!(r"[\w]*" => Identifier),
      ]
    }
  }

  fn tokenize_string(&self, content: String) -> Vec<Token> {
    let mut tokens: Vec<Token> = Vec::new();
    let mut ranges: Vec<Pair<usize, usize>> = Vec::new();

    for pair in self.token_map.iter() {
      let (regex, token_type) = (pair.first, pair.second);

      for m in Regex::new(regex).unwrap().find_iter(&content[..]) {
        // Check if the match is already in the ranges
        // If it is, then we don't need to add it
        // If it isn't, then we add it and add the token_type

        let (start, end) = (m.start(), m.end());

        // Ignore if len is 0
        if end - start == 0 {
          continue
        }

        let mut found = false;
        for range in ranges.iter() {
          if start >= range.first && end <= range.second {
            found = true;
            break
          }
        }

        if !found {
          if token_type != Tokens::Comment {
            tokens.push(Token {
              kind:    token_type,
              content: m.as_str().to_string(),
              line: 0, // This field will be filled later, in the `tokenize_file` function
              column: start
            });
          }
          ranges.push(pair!(m.start() => m.end()));
        }
      }
    }

    tokens.push(Token {
      kind:    Tokens::EOL,
      content: "".to_string(),
      line: 0,
      column: 0
    });

    return tokens
  }

  fn tokenize_file(&self, filepath: &str) -> Vec<Token> {
    let mut tokens: Vec<Token> = Vec::new();
    let mut line_num: usize = 1;

    let file = 
      match File::open(filepath) {
        Ok(file) => file,
        Err(error) => panic!("{}", error)
      };

    let lines = BufReader::new(file).lines();

    for line in lines {
      let mut line_tokens = self.tokenize_string(line.unwrap());
      for token in line_tokens.iter_mut() {
        token.line = line_num;
      }

      tokens.append(&mut line_tokens);
      line_num += 1;
    }

    return tokens
  }

  pub fn tokenize(&mut self) {
    self.stream =
      match self.content {
        ContentType::File(ref file) => self.tokenize_file(file),
        ContentType::String(ref string) => self.tokenize_string(string.to_string())
      }
  }
}
