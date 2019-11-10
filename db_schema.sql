CREATE TABLE paper_info (
    arxiv_id TEXT PRIMARY KEY,
    title TEXT,
    abstract TEXT NOT NULL ,
    published DATE NOT NULL,
    pdf_link TEXT NOT NULL,
    pdf_path TEXT NOT NULL
);

CREATE TABLE citation_graph (
    child_id TEXT,
    parent_id TEXT,
    PRIMARY KEY (child_id, parent_id),
    FOREIGN KEY (child_id) REFERENCES paper_info(arxiv_id)
);

CREATE TABLE paper_author (
    arxiv_id TEXT,
    author TEXT,
    PRIMARY KEY (arxiv_id, author),
    FOREIGN KEY (arxiv_id) REFERENCES paper_info(arxiv_id)
);

CREATE TABLE paper_keyword (
    arvix_id TEXT,
    keyword TEXT,
    PRIMARY KEY (arvix_id, keyword),
    FOREIGN KEY (arvix_id) REFERENCES paper_info(arxiv_id)
);
