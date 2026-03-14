import React, { useState, useEffect } from 'react'
import S from '../style/Post.module.css'

const Post = ({ data }) => {
  const [isLiked, setIsLiked] = useState(data.is_liked) 
  const [likesCount, setLikesCount] = useState(data.likes_count);
  const [isExpanded, setIsExpanded] = useState(false)
  const [comments, setComments] = useState([])

  const date = new Date(data.published_at);
  const formattedDate = date.toLocaleDateString('ru-RU'); 
  const formattedTime = date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' })


  useEffect(() => {
    const fetch_comments = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:8000/api/news/news/${data.id}/comments/`)
            const commentData = await response.json();
            setComments(commentData.results || commentData);
            console.log(comments)
        } 
        catch (error) {
            console.log("Ошибка загрузки комментов:", error)
        }
    } 
    fetch_comments()
  }, [data.id])

    let token = localStorage.getItem('userToken');
    if (token) {
        token = token.replace(/"/g, '').trim(); 
    }

  const handleLike = async (e) => {
    e.stopPropagation()
    
    if (!token) {
        alert("Войдите в систему, чтобы поставить лайк!")
        return
    }


    try {
        const response = await fetch(`http://127.0.0.1:8000/api/news/news/${data.id}/like/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // передача токена если юзер авторизован
                'Authorization': `Bearer ${token}`
            },
        });

        if (response.ok) {
            const result = await response.json();
            // обновление локальное состояния на основе ответа от джанго
            setIsLiked(result.liked);
            setLikesCount(result.likes_count); 
        } else if (response.status === 401) {
            alert("Нужно авторизоваться, чтобы ставить лайки!");
        }
    } catch (error) {
        console.error("Ошибка при лайке:", error);
    }
    }
    
const [commentText, setCommentText] = useState("");

const submitComment = async () => {
    if (!commentText.trim()) return;

    let token = localStorage.getItem('userToken');
    if (token) token = token.replace(/"/g, '').trim();

    if (!token) {
        alert("Войдите, чтобы оставить комментарий");
        return;
    }

    try {
        const response = await fetch(`http://127.0.0.1:8000/api/news/news/${data.id}/comments/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ content: commentText }) 
        });

        if (response.ok) {
            const newComment = await response.json();
            // обновление страницы для вывода нового коммента
            setComments(prev => [...prev, newComment]);
            setCommentText(""); 
        } else {
            const error = await response.json();
            console.error("Ошибка сервера:", error);
            alert("Не удалось отправить комментарий");
        }
    } catch (error) {
        console.error("Ошибка сети:", error);
    }
};

  if (!data) return null;

  return (
		<div className={`${S.news_post} ${isExpanded ? S.expanded : ''}`}>
			<div className={S.post_main}>
				<div className={S.post_header}>
					<div className={S.post_author}>
						<div className={S.author_avatar}>
							{data.author_avatar ? (
								<img
									src={data.author_avatar}
									alt={data.author_name || 'avatar'}
									className={S.avatar_img}
								/>
							) : (
								'👤'
							)}
						</div>
						<div className={S.author_info}>
							<div className={S.author_name}>{data.author_name || 'Админ'}</div>
							<div className={S.post_time}>
								{formattedDate} в {formattedTime}
							</div>
						</div>
					</div>
				</div>

				{/* раскрытие поста */}
				<div
					className={`${S.post_body} ${!isExpanded ? S.clickable : ''}`}
					onClick={() => setIsExpanded(!isExpanded)}
				>
					<h3 className={S.post_title}>{data.title}</h3>

					<div
						className={`${S.excerpt_wrapper} ${!isExpanded ? S.fade_bottom : ''}`}
					>
						<p className={S.post_excerpt}>
							{isExpanded ? data.content : data.short_description}
						</p>
					</div>

					{data.image ? (
						<img src={data.image} alt='post' className={S.post_image} />
					) : (
						<div className={S.post_image_content}>[Изображение]</div>
					)}
				</div>

				<div className={S.post_stats}>
					<button
						className={`${S.stat_item} ${isLiked ? S.liked : ''}`}
						onClick={handleLike}
					>
						<svg
							viewBox='0 0 24 24'
							fill={isLiked ? 'red' : 'transparent'}
							stroke={isLiked ? 'red' : 'currentColor'}
							strokeWidth='2'
							xmlns='http://www.w3.org'
						>
							<path d='M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z' />
						</svg>
						<span>{likesCount}</span>
					</button>
					<div className={S.stat_item}>
						<span>💬 {data.comments_count}</span>
					</div>
					<div className={S.stat_item}>
						<span>👁️ {data.views_count}</span>
					</div>
				</div>
			</div>

			<div className={S.post_comments_sidebar}>
				<h4 className={S.comments_title}>Комментарии ({comments.length})</h4>
				<div className={S.comments_list}>
					{comments.length > 0 ? (
						comments.map(comment => (
							<div key={comment.id} className={S.comment_item}>
								<span className={S.comment_user}>
									{comment.author.username || 'Юзер'}:
								</span>
								{comment.content}
							</div>
						))
					) : (
						<div className={S.comment_item}>
							<span className={S.comment_user}>Система:</span> Комментариев пока
							нет
						</div>
					)}
				</div>
				<div className={S.comment_input_wrapper}>
					<input
						type='text'
						placeholder='Написать комментарий...'
						className={S.comment_input}
						value={commentText}
						onChange={e => setCommentText(e.target.value)}
						// отправка по Enter
						onKeyDown={e => {
							if (e.key === 'Enter') {
								e.preventDefault()
								submitComment()
							}
						}}
					/>
					<button
						className={S.send_comment_btn}
						onClick={submitComment}
						disabled={!commentText.trim()}
					>
						➤
					</button>
				</div>
			</div>
		</div>
	)
}

export default Post
