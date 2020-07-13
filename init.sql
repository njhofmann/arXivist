CREATE TABLE IF NOT EXISTS paper_info (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT,
    abstract TEXT NOT NULL ,
    published DATE NOT NULL,
    pdf_link TEXT NOT NULL,
    pdf_path TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS citation_graph (
    child_id TEXT,
    parent_id TEXT,
    PRIMARY KEY (child_id, parent_id),
    FOREIGN KEY (child_id) REFERENCES paper_info(arxiv_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_author (
    arxiv_id TEXT,
    author TEXT,
    PRIMARY KEY (arxiv_id, author),
    FOREIGN KEY (arxiv_id) REFERENCES paper_info(arxiv_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS paper_keyword (
    arvix_id TEXT,
    keyword TEXT,
    PRIMARY KEY (arvix_id, keyword),
    FOREIGN KEY (arvix_id) REFERENCES paper_info(arxiv_id) ON DELETE CASCADE
);
