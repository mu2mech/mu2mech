/*
 * kv_parser.h — order-independent key-value parser for input.dat
 *
 * File format (one entry per line):
 *   key value
 *   # comment lines (starting with '#') are ignored
 *   blank lines are ignored
 *
 * Keys and values are single whitespace-delimited tokens.
 * The order of lines does not matter — every parameter is looked up by name.
 *
 * Usage:
 *   KVDoc doc = kv_load("input.dat");
 *   double dt = kv_get_double(&doc, "delT");
 *   int    lx = kv_get_int   (&doc, "lx");
 *   char   buf[32];
 *   kv_get_string(&doc, "resumeFrom", buf, sizeof(buf));
 */

#ifndef KV_PARSER_H
#define KV_PARSER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define KV_MAX_ENTRIES  64
#define KV_KEY_LEN      64
#define KV_VAL_LEN     128

typedef struct {
    char key[KV_KEY_LEN];
    char val[KV_VAL_LEN];
} KVEntry;

typedef struct {
    KVEntry entries[KV_MAX_ENTRIES];
    int     count;
} KVDoc;

/* ── Internal helper ──────────────────────────────────────────────────────── */
static inline FILE *kv_fopen_or_die(const char *path, const char *mode)
{
    FILE *f = fopen(path, mode);
    if (!f) {
        fprintf(stderr, "ERROR: cannot open '%s'\n", path);
        exit(EXIT_FAILURE);
    }
    return f;
}

/* ── Parse the file ───────────────────────────────────────────────────────── */
static inline KVDoc kv_load(const char *path)
{
    KVDoc doc;
    doc.count = 0;

    FILE *f = kv_fopen_or_die(path, "r");
    char  line[256];

    while (fgets(line, sizeof(line), f)) {
        /* Skip blank lines and comment lines */
        char *p = line;
        while (*p == ' ' || *p == '\t') p++;
        if (*p == '#' || *p == '\n' || *p == '\r' || *p == '\0')
            continue;

        if (doc.count >= KV_MAX_ENTRIES) {
            fprintf(stderr, "WARNING: input.dat exceeds %d entries; "
                            "raise KV_MAX_ENTRIES if needed\n", KV_MAX_ENTRIES);
            break;
        }

        char key[KV_KEY_LEN], val[KV_VAL_LEN];
        if (sscanf(p, "%63s %127s", key, val) == 2) {
            snprintf(doc.entries[doc.count].key, KV_KEY_LEN, "%s", key);
            snprintf(doc.entries[doc.count].val, KV_VAL_LEN, "%s", val);
            doc.count++;
        }
    }
    fclose(f);
    return doc;
}

/* ── Typed accessors ──────────────────────────────────────────────────────── */

/* Returns the raw value string, or exits with an error if the key is absent. */
static inline const char *kv_get_raw(const KVDoc *doc, const char *key)
{
    for (int i = 0; i < doc->count; i++)
        if (strcmp(doc->entries[i].key, key) == 0)
            return doc->entries[i].val;

    fprintf(stderr, "ERROR: key '%s' not found in input.dat\n", key);
    exit(EXIT_FAILURE);
}

static inline double kv_get_double(const KVDoc *doc, const char *key)
{
    return atof(kv_get_raw(doc, key));
}

static inline int kv_get_int(const KVDoc *doc, const char *key)
{
    return atoi(kv_get_raw(doc, key));
}

static inline void kv_get_string(const KVDoc *doc, const char *key,
                                  char *buf, size_t max_len)
{
    snprintf(buf, max_len, "%s", kv_get_raw(doc, key));
}

#endif /* KV_PARSER_H */
