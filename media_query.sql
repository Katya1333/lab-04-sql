SELECT 
    p.post_id,
    p.title,
    p.posted_at,
    u.username,
    u.email
FROM posts AS p
JOIN users AS u
    ON p.user_id = u.user_id
WHERE p.posted_at >= '2024-02-08'
ORDER BY p.posted_at;