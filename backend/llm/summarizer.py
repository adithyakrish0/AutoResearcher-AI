import requests
import time
import random
from config import LLM_PROVIDER, LLM_API_KEY, MODEL_NAME, GROQ_BASE_URL, OPENAI_BASE_URL, GEMINI_BASE_URL


class Summarizer:
    """
    LLM-based text summarization.
    Supports multiple providers: Groq, OpenAI, Gemini.
    """
    
    def __init__(self):
        self.provider = LLM_PROVIDER.lower()
        self.api_key = LLM_API_KEY
        self.model = MODEL_NAME
        
        # Set base URL based on provider
        self.base_urls = {
            "groq": GROQ_BASE_URL,
            "openai": OPENAI_BASE_URL,
            "gemini": GEMINI_BASE_URL
        }
    
    def summarize_with_groq(self, text):
        """Summarize text using Groq API with rate limit retries."""
        max_retries = 3
        base_delay = 5  # Increased from 2 to 5 for stability
        
        for attempt in range(max_retries + 1):
            try:
                payload = {
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": "You are a concise research summarizer. Provide clear, factual summaries."},
                        {"role": "user", "content": text[:4000]}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                }

                headers = {
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    json=payload,
                    headers=headers,
                    timeout=25
                )

                response.raise_for_status()
                data = response.json()
                return data["choices"][0]["message"]["content"]

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    if attempt < max_retries:
                        delay = base_delay * (2 ** attempt) + random.uniform(0, 1)
                        print(f"[Groq] Rate limit hit (429). Retrying in {delay:.2f}s...")
                        time.sleep(delay)
                        continue
                    else:
                        print(f"[Groq Error] Rate limit exceeded after {max_retries} retries.")
                        return f"Summary unavailable (rate limit): {text[:200]}"
                
                print(f"[Groq Error] Status: {e.response.status_code}, Body: {e.response.text}")
                return f"Summary unavailable (error: {str(e)}): {text[:200]}"
            except Exception as e:
                return f"Summary unavailable (error: {str(e)}): {text[:200]}"
    
    def summarize_with_openai(self, text):
        """Summarize text using OpenAI API."""
        url = f"{self.base_urls['openai']}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a helpful research assistant. Summarize the given text concisely, focusing on key insights and main points."
                },
                {
                    "role": "user",
                    "content": f"Summarize this text:\n\n{text[:4000]}"
                }
            ],
            "temperature": 0.7,
            "max_tokens": 500
        }
        
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        
        result = response.json()
        return result["choices"][0]["message"]["content"]
    
    def summarize_with_gemini(self, text):
        """Summarize text using Google Gemini API."""
        url = f"{self.base_urls['gemini']}/models/{self.model}:generateContent"
        headers = {
            "Content-Type": "application/json"
        }
        params = {
            "key": self.api_key
        }
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Summarize this text concisely, focusing on key insights and main points:\n\n{text[:4000]}"
                }]
            }],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 500
            }
        }
        
        response = requests.post(url, json=payload, headers=headers, params=params)
        response.raise_for_status()
        
        result = response.json()
        return result["candidates"][0]["content"]["parts"][0]["text"]
    
    def summarize(self, text):
        """
        Summarize the given text using the configured LLM provider.
        
        Args:
            text (str): The text to summarize
            
        Returns:
            str: AI-generated summary
        """
        if not text:
            return "No text provided for summary"
        
        # Check if API key is available
        if not self.api_key:
            # Fallback to truncated text
            max_length = 200
            if len(text) > max_length:
                return f"Summary unavailable (no API key): {text[:max_length]}..."
            else:
                return f"Summary unavailable (no API key): {text}"
        
        try:
            # Call appropriate provider
            if self.provider == "groq":
                return self.summarize_with_groq(text)
            elif self.provider == "openai":
                return self.summarize_with_openai(text)
            elif self.provider == "gemini":
                return self.summarize_with_gemini(text)
            else:
                return f"Summary unavailable (unknown provider '{self.provider}'): {text[:200]}..."
                
        except Exception as e:
            # Fallback on error
            max_length = 200
            error_msg = f"Summary unavailable (error: {str(e)}): "
            if len(text) > max_length:
                return error_msg + text[:max_length] + "..."
            else:
                return error_msg + text

    def summarize_multi_source(self, text, provider="groq"):
        """
        Summarize merged text from multiple sources using chunking.
        Handles large inputs by splitting, summarizing chunks, and condensing.
        """
        if not text or len(text.strip()) == 0:
            return "No content available"

        print(f"[MultiSource] Summarizing text of length {len(text)}...")

        # Chunk size (Groq max safe input ~3500 chars)
        CHUNK_SIZE = 3000

        chunks = [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]
        
        # --- HACKATHON STABILITY FIX ---
        # Cap at 5 chunks to avoid Rate Limits (429) during demo
        if len(chunks) > 5:
            print(f"[MultiSource] Capping chunks from {len(chunks)} to 5 for stability.")
            chunks = chunks[:5]
        # -------------------------------
        
        print(f"[MultiSource] Split into {len(chunks)} chunks")

        partial_summaries = []
        for idx, chunk in enumerate(chunks):
            # Proactive delay to avoid rate limits
            if idx > 0:
                time.sleep(5)  # Increased from 2s to 5s

            try:
                print(f"[MultiSource] Summarizing chunk {idx+1}/{len(chunks)}...")
                summary = self.summarize(chunk)
                
                # Check if summarize() returned an error string
                if summary.startswith("Summary unavailable (error:"):
                    print(f"[MultiSource] Chunk summary failed: {summary}")
                    continue
                    
                partial_summaries.append(summary)
            except Exception as e:
                print(f"[MultiSource] Error summarizing chunk {idx}: {e}")
                # Skip failed chunks to avoid polluting the summary with error strings
                pass

        # Combine partial summaries
        combined = "\n\n".join(partial_summaries)
        print(f"[MultiSource] Combined partial summaries length: {len(combined)}")

        # HARD LENGTH CAP
        combined = combined[:4000]  # make absolutely sure Groq never rejects

        # Final condensation step
        try:
            print("[MultiSource] Generating final condensed summary...")
            final_prompt = "Combine and condense these summaries into a unified, short, bullet-point overview:\n\n" + combined
            
            final_summary = self.summarize(final_prompt)
            
            # Check if final summary returned an error string
            if final_summary.startswith("Summary unavailable (error:"):
                print(f"[MultiSource] Final summary returned error: {final_summary}")
                return combined
                
            return final_summary
        except Exception as e:
            print(f"[MultiSource] Final summary failed: {e}")
            return combined  # fallback to partials without error text
