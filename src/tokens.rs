use std::fmt::{Display, Error, Formatter};

use regex::Regex;

macro_rules! pair {
  ($a:expr => $b:expr) => {
    Pair {
      first:  $a,
      second: $b
    }
  };
}

#[derive(Copy, Clone)]
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
  Comment
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
      Comment => "Comment"
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
  pub content: String
}

impl Token {
  pub fn new(
    kind: Tokens,
    content: String
  ) -> Self {
    Token {
      kind,
      content
    }
  }
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

pub struct Tokenizer {
  token_map: Vec<Pair<&'static str, Tokens>>,
  content:   String
}

impl Tokenizer {
  pub fn new(content: String) -> Tokenizer {
    use Tokens::*;
    Tokenizer {
      content,
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

  pub fn tokenize(&self) -> Vec<Token> {
    let mut tokens: Vec<Token> = Vec::new();
    let mut ranges: Vec<Pair<usize, usize>> = Vec::new();

    for pair in self.token_map.iter() {
      let (regex, token) = (pair.first, pair.second);

      for m in Regex::new(regex).unwrap().find_iter(&self.content) {
        // Check if the match is already in the ranges
        // If it is, then we don't need to add it
        // If it isn't, then we add it and add the token

        // Ignore if len is 0
        if m.end() - m.start() == 0 {
          continue
        }

        let mut found = false;
        for range in ranges.iter() {
          if m.start() >= range.first && m.end() <= range.second {
            found = true;
            break
          }
        }

        if !found {
          tokens.push(Token::new(token, m.as_str().to_string()));
          ranges.push(pair!(m.start() => m.end()));
        }
      }
    }

    return tokens
  }
}
