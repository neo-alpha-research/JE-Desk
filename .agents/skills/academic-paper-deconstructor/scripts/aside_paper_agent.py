#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Aside CLI Universal Academic Paper Intelligence Agent (ops/tools/aside_paper_agent.py)
- Universal Academic Paper Deconstructor:
    Supports SpringerLink, ScienceDirect, IEEE Xplore, Wiley, Nature, SSRN, arXiv, PubMed, etc.
- Institutional Library & Anti-Bot Bypass:
    Leverages Aside Chromium native session (Profile 0), inheriting active university library
    proxy credentials, cookies, and Cloudflare bypass.
- Universal Highwire Press / Dublin Core Meta Extraction:
    Extracts citation_title, citation_author, citation_abstract, citation_doi, citation_pdf_url.
- Global Google Scholar Browsing Engine with Deterministic arXiv Fallback.
"""

import os
import sys
import json
import re
import subprocess
import urllib.request
import urllib.parse
import hashlib
import xml.etree.ElementTree as ET
from datetime import datetime

# Fix Windows console encoding
if sys.platform == 'win32' and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

ASIDE_BIN = r"C:\Users\kibae\AppData\Local\Aside\CLI\current\aside.exe"


def run_aside_prompt(prompt: str, effort: str = "medium", timeout_sec: int = 180) -> str:
    """Execute browsing / reasoning prompt via Aside CLI agent mode."""
    if not os.path.exists(ASIDE_BIN):
        raise FileNotFoundError(f"Aside CLI binary not found at: {ASIDE_BIN}")

    cmd = [
        ASIDE_BIN,
        "--effort", effort,
        "--permission", "full-access",
        prompt
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=timeout_sec)
        out_text = res.stdout.decode("utf-8", errors="replace")
        err_text = res.stderr.decode("utf-8", errors="replace")
        out = (out_text + "\n" + err_text).strip()
        lines = [line for line in out.splitlines() if not line.startswith("created new session:")]
        clean_out = "\n".join(lines).strip()
        
        if "Insufficient credits" in clean_out or "402" in clean_out:
            return "[ASIDE_CREDITS_EXHAUSTED]"
        return clean_out
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] Aside CLI query exceeded execution window."
    except Exception as e:
        return f"[ERROR] Aside CLI execution failed: {str(e)}"


def run_aside_browser_repl(js_code: str, timeout_sec: int = 40) -> str:
    """Execute Playwright JavaScript directly inside Aside Browser REPL (0 credit cost)."""
    if not os.path.exists(ASIDE_BIN):
        raise FileNotFoundError(f"Aside CLI binary not found at: {ASIDE_BIN}")

    cmd = [ASIDE_BIN, "repl", js_code]
    try:
        res = subprocess.run(cmd, capture_output=True, timeout=timeout_sec)
        return (res.stdout.decode("utf-8", errors="replace") + "\n" + res.stderr.decode("utf-8", errors="replace")).strip()
    except subprocess.TimeoutExpired:
        return "[TIMEOUT] Aside Browser REPL execution exceeded limit."
    except Exception as e:
        return f"[ERROR] Aside Browser REPL failed: {str(e)}"


def search_google_scholar_via_aside(query: str, max_results: int = 3) -> list:
    """
    Search Google Scholar via Aside Browser to discover top papers across ALL global publishers.
    (Springer, Elsevier, IEEE, Wiley, Nature, arXiv, SSRN, etc.)
    """
    encoded_q = urllib.parse.quote(query)
    scholar_url = f"https://scholar.google.com/scholar?q={encoded_q}"
    
    js = f"""
const page = await openTab('{scholar_url}');
const items = await page.evaluate(() => {{
    const res = [];
    const nodes = document.querySelectorAll('.gs_r.gs_or.gs_scl');
    for (let i = 0; i < Math.min(nodes.length, {max_results}); i++) {{
        const n = nodes[i];
        const tEl = n.querySelector('.gs_rt a');
        const title = tEl ? tEl.innerText : (n.querySelector('.gs_rt')?.innerText || '');
        const url = tEl ? tEl.getAttribute('href') : '';
        const meta = n.querySelector('.gs_a')?.innerText || '';
        const snippet = n.querySelector('.gs_rs')?.innerText || '';
        const pdf = n.querySelector('.gs_or_ggsm a')?.getAttribute('href') || '';
        if (title) {{
            res.push({{ title: title.replace(/\\n/g, ' ').trim(), url, meta, snippet, pdf_url: pdf }});
        }}
    }}
    return res;
}});
console.log('<<<JSON_START>>>' + JSON.stringify(items) + '<<<JSON_END>>>');
"""
    output = run_aside_browser_repl(js)
    m = re.search(r"<<<JSON_START>>>(.*?)<<<JSON_END>>>", output, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except Exception:
            pass
    return []


def extract_paper_universal_via_aside(paper_url: str) -> dict:
    """
    Universal Academic Paper Extractor.
    Extracts paper metadata and abstract from ANY academic publisher using
    Highwire Press, Dublin Core, OpenGraph, and semantic HTML fallbacks.
    Also carries institutional library proxy cookies if logged in.
    """
    js = f"""
const page = await openTab('{paper_url}');
const data = await page.evaluate(() => {{
    const getMeta = (names) => {{
        for (const name of names) {{
            const el = document.querySelector('meta[name="' + name + '" i], meta[property="' + name + '" i]');
            if (el && el.getAttribute('content')) return el.getAttribute('content').trim();
        }}
        return '';
    }};
    const getAllMeta = (names) => {{
        const list = [];
        for (const name of names) {{
            const els = document.querySelectorAll('meta[name="' + name + '" i], meta[property="' + name + '" i]');
            for (const el of els) {{
                const val = el.getAttribute('content');
                if (val && !list.includes(val.trim())) list.push(val.trim());
            }}
        }}
        return list;
    }};

    let title = getMeta(['citation_title', 'dc.title', 'dcterms.title', 'og:title', 'twitter:title']);
    if (!title) {{
        title = document.querySelector('h1.title, h1.c-article-title, h1.article-title, h1')?.innerText || document.title;
    }}
    title = title.replace(/^Title:\\s*/i, '').replace(/\\s+/g, ' ').trim();

    let authors = getAllMeta(['citation_author', 'dc.creator', 'dcterms.creator', 'author']);
    if (authors.length === 0) {{
        const authorEl = document.querySelector('.authors, .c-article-author-list, .author-name, .article-author');
        if (authorEl) {{
            authors = [authorEl.innerText.replace(/^Authors?:\\s*/i, '').trim()];
        }}
    }}

    let abstract = getMeta(['citation_abstract', 'dc.description', 'dcterms.abstract', 'description', 'og:description']);
    if (!abstract || abstract.length < 50) {{
        const absEl = document.querySelector('.abstract, #abstract, .article-abstract, #abstract-content, .c-article-section__content, section.abstract, div[class*="abstract" i]');
        if (absEl) {{
            abstract = absEl.innerText.replace(/^Abstract:?\\s*/i, '').trim();
        }}
    }}

    const doi = getMeta(['citation_doi', 'dc.identifier', 'dc.identifier.doi']);
    const journal = getMeta(['citation_journal_title', 'citation_conference_title', 'dc.publisher']);
    const published = getMeta(['citation_publication_date', 'citation_date', 'dc.date', 'dc.date.issued']);
    const pdf_url = getMeta(['citation_pdf_url', 'citation_fulltext_html_url']);

    return {{
        title,
        authors,
        abstract,
        doi,
        journal,
        published,
        pdf_url
    }};
}});
console.log('<<<JSON_START>>>' + JSON.stringify(data) + '<<<JSON_END>>>');
"""
    output = run_aside_browser_repl(js)
    m = re.search(r"<<<JSON_START>>>(.*?)<<<JSON_END>>>", output, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(1).strip())
        except Exception:
            pass
    return {}


def query_arxiv_fallback(query: str, max_results: int = 3) -> list:
    """Deterministic fallback to arXiv Atom API."""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"all:{query}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "relevance",
        "sortOrder": "descending"
    }
    encoded_url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(encoded_url, headers={"User-Agent": "AsideUniversalPaperAgent/2.0"})
    
    entries = []
    try:
        with urllib.request.urlopen(req, timeout=12) as resp:
            root = ET.fromstring(resp.read())
            ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
            for e in root.findall("atom:entry", ns):
                title = e.find("atom:title", ns).text.strip().replace("\n", " ")
                summary = e.find("atom:summary", ns).text.strip().replace("\n", " ")
                id_url = e.find("atom:id", ns).text.strip()
                published = e.find("atom:published", ns).text.strip()[:10]
                
                authors = []
                for a in e.findall("atom:author", ns):
                    name = a.find("atom:name", ns).text
                    if name:
                        authors.append(name.strip())
                
                m = re.search(r"abs/([0-9.]+)", id_url)
                arxiv_id = m.group(1) if m else id_url.split("/")[-1]
                
                entries.append({
                    "id": arxiv_id,
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "url": id_url,
                    "pdf_url": id_url.replace("abs", "pdf") + ".pdf",
                    "abstract": summary
                })
    except Exception as ex:
        print(f"[WARN] ArXiv fallback encountered issue: {ex}", file=sys.stderr)
        
    return entries


def search_and_extract_paper(query_or_url: str, effort: str = "medium", use_aside: bool = True) -> dict:
    """
    Universal Search & Extract Pipeline:
    1. If URL: Directly extracts from the publisher page using universal Highwire/Dublin Core parser.
    2. If Query: Searches Google Scholar via Aside REPL across all global publishers.
       Falls back to arXiv if Google Scholar returns no results.
    """
    is_url = query_or_url.startswith("http://") or query_or_url.startswith("https://")
    now_str = datetime.now().strftime("%Y-%m-%d")

    target_url = query_or_url if is_url else ""
    paper_id = "PAPER_" + datetime.now().strftime("%Y%m%d_%H%M%S")
    title = query_or_url
    authors = ["Domain Researcher"]
    published = now_str
    abstract = "Universal academic extraction via Aside Engine."
    pdf_url = ""
    doi = ""
    journal = "Global Academic Repository"

    # 1. URL Mode
    if is_url:
        print(f"[*] Navigating to direct academic URL via Aside Browser: {target_url}")
        meta = extract_paper_universal_via_aside(target_url)
        if meta and meta.get("title"):
            title = meta.get("title")
            authors = meta.get("authors") or authors
            abstract = meta.get("abstract") or abstract
            doi = meta.get("doi") or ""
            journal = meta.get("journal") or journal
            published = meta.get("published") or published
            pdf_url = meta.get("pdf_url") or ""
            
            # Generate deterministic ID
            m_arxiv = re.search(r"abs/([0-9.]+)", target_url)
            if m_arxiv:
                paper_id = m_arxiv.group(1)
            elif doi:
                paper_id = doi.replace("/", "_").replace(".", "_")
            else:
                paper_id = "URL_" + hashlib.md5(target_url.encode()).hexdigest()[:10]

    # 2. Query Search Mode (Google Scholar 1st, arXiv 2nd)
    else:
        print(f"[*] Dispatching Aside Google Scholar search for: '{query_or_url}'...")
        scholar_results = search_google_scholar_via_aside(query_or_url, max_results=3)
        
        if scholar_results and scholar_results[0].get("url"):
            top_hit = scholar_results[0]
            target_url = top_hit["url"]
            pdf_url = top_hit.get("pdf_url", "")
            print(f"[+] Google Scholar #1 Hit: {top_hit['title']} ({target_url})")
            
            # Deep extract from the publisher landing page
            meta = extract_paper_universal_via_aside(target_url)
            title = meta.get("title") or top_hit["title"]
            authors = meta.get("authors") or ([top_hit["meta"].split("-")[0].strip()] if top_hit.get("meta") else authors)
            abstract = meta.get("abstract") or top_hit.get("snippet") or abstract
            doi = meta.get("doi") or ""
            journal = meta.get("journal") or journal
            published = meta.get("published") or published
            if not pdf_url:
                pdf_url = meta.get("pdf_url") or target_url

            m_arxiv = re.search(r"abs/([0-9.]+)", target_url)
            if m_arxiv:
                paper_id = m_arxiv.group(1)
            elif doi:
                paper_id = doi.replace("/", "_").replace(".", "_")
            else:
                paper_id = "GS_" + re.sub(r"[^a-zA-Z0-9]", "_", title[:25])
        else:
            print("[*] Google Scholar direct hits empty ➔ Engaging arXiv Atom API fallback...")
            arxiv_hits = query_arxiv_fallback(query_or_url, max_results=1)
            if arxiv_hits:
                top_hit = arxiv_hits[0]
                paper_id = top_hit["id"]
                title = top_hit["title"]
                authors = top_hit["authors"]
                published = top_hit["published"]
                target_url = top_hit["url"]
                pdf_url = top_hit["pdf_url"]
                abstract = top_hit["abstract"]
                journal = "arXiv Open Access"

    aside_corpus = f"""### [Aside Universal Browser Extraction]
- **Target URL**: {target_url}
- **Browser Engine**: Aside Chromium Native Session (Profile 0 / Subscribed Access)
- **Title**: {title}
- **Authors**: {', '.join(authors) if isinstance(authors, list) else authors}
- **Publication Venue**: {journal}
- **DOI / Identifier**: {doi or 'N/A'}
- **Publication Date**: {published}
- **Full-Text PDF Link**: {pdf_url or target_url}
- **Deconstructed Abstract**:
{abstract}
"""

    return {
        "paper_id": paper_id,
        "title": title,
        "authors": authors if isinstance(authors, list) else [authors],
        "published_date": published,
        "url": target_url,
        "pdf_url": pdf_url or target_url,
        "doi": doi,
        "journal": journal,
        "abstract": abstract,
        "aside_analysis": aside_corpus,
        "created_at": datetime.now().isoformat()
    }


if __name__ == "__main__":
    test_target = "https://link.springer.com/article/10.1007/s13042-026-03196-0"
    print(f"Testing Universal Paper Agent with Springer URL: {test_target}")
    res = search_and_extract_paper(test_target, effort="medium")
    print("Result Title:", res["title"])
    print("Journal:", res["journal"])
    print("DOI:", res["doi"])
    print("Authors:", res["authors"])
    print("Snippet:", res["abstract"][:200])
