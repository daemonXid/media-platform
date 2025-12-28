//! # DAEMON-ONE Core - Rust Accelerator
//!
//! High-performance Rust module for AI preprocessing and CPU-intensive tasks.
//! Exposed to Python via PyO3 with zero-copy when possible.
//!
//! ## When to use Rust:
//! - Token counting (tiktoken)
//! - Text preprocessing (cleaning, chunking)
//! - Vector similarity search
//! - Batch data transformations
//! - Financial calculations
//!
//! ## When NOT to use Rust:
//! - Simple CRUD operations
//! - HTTP request handling (let Django do it)
//! - Database queries

use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;
use rayon::prelude::*;

// ============================================
// 🎯 Basic Functions
// ============================================

/// Hello from Rust - basic test function
#[pyfunction]
fn rust_hello() -> PyResult<String> {
    Ok("Hello from DAEMON-ONE Rust Core! 🦀😈".to_string())
}

/// Fast sum using Rust - demo of basic acceleration
#[pyfunction]
fn fast_sum(numbers: Vec<i64>) -> PyResult<i64> {
    Ok(numbers.par_iter().sum())
}

/// Fibonacci calculation - CPU-intensive demo
#[pyfunction]
fn fibonacci(n: u64) -> PyResult<u64> {
    fn fib(n: u64) -> u64 {
        if n <= 1 { n } else { fib(n - 1) + fib(n - 2) }
    }
    
    if n > 50 {
        return Err(PyValueError::new_err("n must be <= 50 to avoid overflow"));
    }
    Ok(fib(n))
}

// ============================================
// 🤖 AI Preprocessing Functions
// ============================================

/// Count tokens approximately (simplified tiktoken-like)
/// Use this before sending to AI API to estimate costs
#[pyfunction]
fn count_tokens_approx(text: &str) -> PyResult<usize> {
    // Approximate: ~4 chars per token for English, ~2 for Korean
    let char_count = text.chars().count();
    
    // Check if mostly Korean (rough heuristic)
    let korean_chars = text.chars().filter(|c| {
        let code = *c as u32;
        (0xAC00..=0xD7AF).contains(&code) || // Hangul Syllables
        (0x1100..=0x11FF).contains(&code) || // Hangul Jamo
        (0x3130..=0x318F).contains(&code)    // Hangul Compatibility Jamo
    }).count();
    
    let korean_ratio = korean_chars as f64 / char_count.max(1) as f64;
    
    if korean_ratio > 0.3 {
        // Korean: ~2 chars per token
        Ok(char_count / 2 + 1)
    } else {
        // English: ~4 chars per token
        Ok(char_count / 4 + 1)
    }
}

/// Clean and normalize text for AI input
#[pyfunction]
fn clean_text_for_ai(text: &str) -> PyResult<String> {
    let cleaned: String = text
        .lines()
        .map(|line| line.trim())
        .filter(|line| !line.is_empty())
        .collect::<Vec<_>>()
        .join("\n");
    
    // Remove excessive whitespace
    let re = regex::Regex::new(r"\s+").unwrap();
    let result = re.replace_all(&cleaned, " ");
    
    Ok(result.trim().to_string())
}

/// Chunk text for AI processing (respects sentence boundaries)
#[pyfunction]
fn chunk_text(text: &str, max_tokens: usize) -> PyResult<Vec<String>> {
    let sentences: Vec<&str> = text
        .split(|c| c == '.' || c == '!' || c == '?' || c == '\n')
        .filter(|s| !s.trim().is_empty())
        .collect();
    
    let mut chunks: Vec<String> = Vec::new();
    let mut current_chunk = String::new();
    let mut current_tokens = 0;
    
    for sentence in sentences {
        let sentence = sentence.trim();
        let sentence_tokens = sentence.len() / 4 + 1; // approx
        
        if current_tokens + sentence_tokens > max_tokens && !current_chunk.is_empty() {
            chunks.push(current_chunk.trim().to_string());
            current_chunk = String::new();
            current_tokens = 0;
        }
        
        current_chunk.push_str(sentence);
        current_chunk.push_str(". ");
        current_tokens += sentence_tokens;
    }
    
    if !current_chunk.trim().is_empty() {
        chunks.push(current_chunk.trim().to_string());
    }
    
    Ok(chunks)
}

// ============================================
// 📊 Vector Operations (for embeddings)
// ============================================

/// Cosine similarity between two vectors
#[pyfunction]
fn cosine_similarity(vec1: Vec<f64>, vec2: Vec<f64>) -> PyResult<f64> {
    if vec1.len() != vec2.len() {
        return Err(PyValueError::new_err("Vectors must have same length"));
    }
    
    let dot: f64 = vec1.iter().zip(vec2.iter()).map(|(a, b)| a * b).sum();
    let norm1: f64 = vec1.iter().map(|x| x * x).sum::<f64>().sqrt();
    let norm2: f64 = vec2.iter().map(|x| x * x).sum::<f64>().sqrt();
    
    if norm1 == 0.0 || norm2 == 0.0 {
        return Ok(0.0);
    }
    
    Ok(dot / (norm1 * norm2))
}

/// Find top-k most similar vectors (batch operation)
#[pyfunction]
fn find_top_k_similar(
    query: Vec<f64>,
    vectors: Vec<Vec<f64>>,
    k: usize,
) -> PyResult<Vec<(usize, f64)>> {
    let mut similarities: Vec<(usize, f64)> = vectors
        .par_iter()
        .enumerate()
        .map(|(i, vec)| {
            let dot: f64 = query.iter().zip(vec.iter()).map(|(a, b)| a * b).sum();
            let norm1: f64 = query.iter().map(|x| x * x).sum::<f64>().sqrt();
            let norm2: f64 = vec.iter().map(|x| x * x).sum::<f64>().sqrt();
            let sim = if norm1 == 0.0 || norm2 == 0.0 { 0.0 } else { dot / (norm1 * norm2) };
            (i, sim)
        })
        .collect();
    
    similarities.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());
    similarities.truncate(k);
    
    Ok(similarities)
}

// ============================================
// 💰 Financial Calculations
// ============================================

/// Compound interest calculation
#[pyfunction]
fn compound_interest(principal: f64, rate: f64, years: u32, compounds_per_year: u32) -> PyResult<f64> {
    let n = compounds_per_year as f64;
    let t = years as f64;
    let result = principal * (1.0 + rate / n).powf(n * t);
    Ok((result * 100.0).round() / 100.0)
}

/// Calculate multiple scenarios in parallel
#[pyfunction]
fn batch_compound_interest(
    principals: Vec<f64>,
    rate: f64,
    years: u32,
    compounds_per_year: u32,
) -> PyResult<Vec<f64>> {
    let n = compounds_per_year as f64;
    let t = years as f64;
    
    let results: Vec<f64> = principals
        .par_iter()
        .map(|p| {
            let result = p * (1.0 + rate / n).powf(n * t);
            (result * 100.0).round() / 100.0
        })
        .collect();
    
    Ok(results)
}

// ============================================
// 🔧 Module Registration
// ============================================

#[pymodule]
fn daemon_one_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Basic
    m.add_function(wrap_pyfunction!(rust_hello, m)?)?;
    m.add_function(wrap_pyfunction!(fast_sum, m)?)?;
    m.add_function(wrap_pyfunction!(fibonacci, m)?)?;
    
    // AI Preprocessing
    m.add_function(wrap_pyfunction!(count_tokens_approx, m)?)?;
    m.add_function(wrap_pyfunction!(clean_text_for_ai, m)?)?;
    m.add_function(wrap_pyfunction!(chunk_text, m)?)?;
    
    // Vector Operations
    m.add_function(wrap_pyfunction!(cosine_similarity, m)?)?;
    m.add_function(wrap_pyfunction!(find_top_k_similar, m)?)?;
    
    // Financial
    m.add_function(wrap_pyfunction!(compound_interest, m)?)?;
    m.add_function(wrap_pyfunction!(batch_compound_interest, m)?)?;
    
    Ok(())
}
