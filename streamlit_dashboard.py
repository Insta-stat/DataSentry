import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from config import stdev_hot_treshold, stdev_very_successful_treshold

df = pd.read_csv('raw_data/described_data.csv')
df = df.sort_values(by='timestamp', ascending=False)

selected_account = st.selectbox("Выбери аккаунт", df['accountName'].unique())
filtered_df = df[df['accountName'] == selected_account]
st.divider()

tab1, tab2, tab3 = st.tabs(["📊 Общая статистика", "📊 Метрики детально", "📹 Видео"])
with tab1:
    st.subheader(f"Общая статистика для аккаунта: {selected_account}")
    
    # Блок "Просмотры"
    st.write("**Просмотры:**")
    
    # Получаем данные о просмотрах
    views_data = filtered_df['videoPlayCount'].dropna()
    
    if len(views_data) > 0:
        # Создаем две колонки для метрик просмотров
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Общее количество просмотров", f"{views_data.sum():,.0f}")
            st.metric("Среднее количество просмотров", f"{views_data.mean():,.1f}")
        
        with col2:
            st.metric("Медиана", f"{views_data.median():,.1f}")
            st.metric("Минимум", f"{views_data.min():,.0f}")
        
        # Добавляем максимум в отдельную строку для лучшего отображения
        st.metric("Максимум", f"{views_data.max():,.0f}")
        
        # График просмотров по дате
        st.write("**График просмотров по времени:**")
        
        # Создаем график просмотров
        fig_views = px.line(
            filtered_df.sort_values('timestamp'),
            x='timestamp',
            y='videoPlayCount',
            title=f"Просмотры по времени для аккаунта {selected_account}",
            markers=True
        )
        
        fig_views.update_traces(
            line=dict(color='rgb(31, 119, 180)'),
            marker=dict(color='white', size=8, line=dict(width=2, color='rgb(31, 119, 180)'))
        )
        
        fig_views.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=[
                        dict(step="all", label="Все"),
                        dict(count=30, label="30д", step="day", stepmode="backward"),
                        dict(count=60, label="60д", step="day", stepmode="backward"),
                        dict(count=90, label="90д", step="day", stepmode="backward"),
                        dict(count=180, label="180д", step="day", stepmode="backward")
                    ]
                ),
            ),
            yaxis=dict(autorange=True)
        )
        
        st.plotly_chart(fig_views, use_container_width=True)
        
    else:
        st.warning("Нет данных о просмотрах")
    
    st.divider()
    
    # Блок "Лайки"
    st.write("**Лайки:**")
    
    # Получаем данные о лайках
    likes_data = filtered_df['likesCount'].dropna()
    views_data_for_rate = filtered_df['videoPlayCount'].dropna()
    
    if len(likes_data) > 0:
        # Создаем две колонки для метрик лайков
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Общее количество лайков", f"{likes_data.sum():,.0f}")
            st.metric("Среднее количество лайков", f"{likes_data.mean():,.1f}")
            # Рассчитываем LikeRate
            total_likes = likes_data.sum()
            total_views = views_data_for_rate.sum()
            like_rate = (total_likes / total_views * 100) if total_views > 0 else 0
            st.metric("LikeRate (лайки/просмотры)", f"{like_rate:.2f}%")
        
        with col2:
            st.metric("Медиана", f"{likes_data.median():,.1f}")
            st.metric("Минимум", f"{likes_data.min():,.0f}")
            st.metric("Максимум", f"{likes_data.max():,.0f}")
        
        # График лайков по дате
        st.write("**График лайков по времени:**")
        
        # Создаем график лайков
        fig_likes = px.line(
            filtered_df.sort_values('timestamp'),
            x='timestamp',
            y='likesCount',
            title=f"Лайки по времени для аккаунта {selected_account}",
            markers=True
        )
        
        fig_likes.update_traces(
            line=dict(color='rgb(220, 53, 69)'),
            marker=dict(color='white', size=8, line=dict(width=2, color='rgb(220, 53, 69)'))
        )
        
        fig_likes.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=[
                        dict(step="all", label="Все"),
                        dict(count=30, label="30д", step="day", stepmode="backward"),
                        dict(count=60, label="60д", step="day", stepmode="backward"),
                        dict(count=90, label="90д", step="day", stepmode="backward"),
                        dict(count=180, label="180д", step="day", stepmode="backward")
                    ]
                ),
            ),
            yaxis=dict(autorange=True)
        )
        
        st.plotly_chart(fig_likes, use_container_width=True)
        
        # График LikeRate по дате
        st.write("**График LikeRate по времени:**")
        
        # Используем готовую колонку likeRate (умножаем на 100 для процентов)
        filtered_df_with_rate = filtered_df.copy()
        filtered_df_with_rate['likeRatePercent'] = filtered_df_with_rate['likeRate'] * 100
        
        # Создаем график LikeRate
        fig_like_rate = px.line(
            filtered_df_with_rate.sort_values('timestamp'),
            x='timestamp',
            y='likeRatePercent',
            title=f"LikeRate по времени для аккаунта {selected_account}",
            markers=True
        )
        
        fig_like_rate.update_traces(
            line=dict(color='rgb(255, 193, 7)'),
            marker=dict(color='white', size=8, line=dict(width=2, color='rgb(255, 193, 7)'))
        )
        
        fig_like_rate.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=[
                        dict(step="all", label="Все"),
                        dict(count=30, label="30д", step="day", stepmode="backward"),
                        dict(count=60, label="60д", step="day", stepmode="backward"),
                        dict(count=90, label="90д", step="day", stepmode="backward"),
                        dict(count=180, label="180д", step="day", stepmode="backward")
                    ]
                ),
            ),
            yaxis=dict(autorange=True, title="LikeRate (%)")
        )
        
        st.plotly_chart(fig_like_rate, use_container_width=True)
        
    else:
        st.warning("Нет данных о лайках")
    
    st.divider()
    
    # Блок "Комментарии"
    st.write("**Комментарии:**")
    
    # Получаем данные о комментариях
    comments_data = filtered_df['commentsCount'].dropna()
    views_data_for_comment_rate = filtered_df['videoPlayCount'].dropna()
    likes_data_for_like_comment_rate = filtered_df['likesCount'].dropna()
    
    if len(comments_data) > 0:
        # Создаем две колонки для метрик комментариев
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Общее количество комментариев", f"{comments_data.sum():,.0f}")
            st.metric("Среднее количество комментариев", f"{comments_data.mean():,.1f}")
            # Рассчитываем CommentRate
            total_comments = comments_data.sum()
            total_views = views_data_for_comment_rate.sum()
            comment_rate = (total_comments / total_views * 100) if total_views > 0 else 0
            st.metric("CommentRate (комменты/просмотры)", f"{comment_rate:.2f}%")
        
        with col2:
            # Рассчитываем Like-CommentRate (комментарии/лайки)
            total_likes = likes_data_for_like_comment_rate.sum()
            like_comment_rate = (total_comments / total_likes * 100) if total_likes > 0 else 0
            st.metric("Like-CommentRate (комменты/лайки)", f"{like_comment_rate:.2f}%")
            st.metric("Медиана", f"{comments_data.median():,.1f}")
            st.metric("Минимум", f"{comments_data.min():,.0f}")
        
        # Добавляем максимум в отдельную строку для лучшего отображения
        st.metric("Максимум", f"{comments_data.max():,.0f}")
        
        # График комментариев по дате
        st.write("**График комментариев по времени:**")
        
        # Создаем график комментариев
        fig_comments = px.line(
            filtered_df.sort_values('timestamp'),
            x='timestamp',
            y='commentsCount',
            title=f"Комментарии по времени для аккаунта {selected_account}",
            markers=True
        )
        
        fig_comments.update_traces(
            line=dict(color='rgb(40, 167, 69)'),
            marker=dict(color='white', size=8, line=dict(width=2, color='rgb(40, 167, 69)'))
        )
        
        fig_comments.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=[
                        dict(step="all", label="Все"),
                        dict(count=30, label="30д", step="day", stepmode="backward"),
                        dict(count=60, label="60д", step="day", stepmode="backward"),
                        dict(count=90, label="90д", step="day", stepmode="backward"),
                        dict(count=180, label="180д", step="day", stepmode="backward")
                    ]
                ),
            ),
            yaxis=dict(autorange=True)
        )
        
        st.plotly_chart(fig_comments, use_container_width=True)
        
        # График CommentRate по дате
        st.write("**График CommentRate по времени:**")
        
        # Используем готовую колонку commentRate (умножаем на 100 для процентов)
        filtered_df_with_comment_rate = filtered_df.copy()
        filtered_df_with_comment_rate['commentRatePercent'] = filtered_df_with_comment_rate['commentRate'] * 100
        
        # Создаем график CommentRate
        fig_comment_rate = px.line(
            filtered_df_with_comment_rate.sort_values('timestamp'),
            x='timestamp',
            y='commentRatePercent',
            title=f"CommentRate по времени для аккаунта {selected_account}",
            markers=True
        )
        
        fig_comment_rate.update_traces(
            line=dict(color='rgb(108, 117, 125)'),
            marker=dict(color='white', size=8, line=dict(width=2, color='rgb(108, 117, 125)'))
        )
        
        fig_comment_rate.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=[
                        dict(step="all", label="Все"),
                        dict(count=30, label="30д", step="day", stepmode="backward"),
                        dict(count=60, label="60д", step="day", stepmode="backward"),
                        dict(count=90, label="90д", step="day", stepmode="backward"),
                        dict(count=180, label="180д", step="day", stepmode="backward")
                    ]
                ),
            ),
            yaxis=dict(autorange=True, title="CommentRate (%)")
        )
        
        st.plotly_chart(fig_comment_rate, use_container_width=True)
        
        # Рассчитываем Like-CommentRate для каждого видео (комментарии/лайки)
        filtered_df_with_like_comment_rate = filtered_df.copy()
        
        # Улучшенный расчет с защитой от экстремальных значений
        def safe_comment_rate_calculation(row):
            likes = row['likesCount']
            comments = row['commentsCount']
            
            # Если лайков меньше 5, считаем соотношение ненадежным
            if likes < 5:
                return 0  # или np.nan для исключения из графика
            
            ratio = (comments / likes) * 100
            
            # Ограничиваем максимальное соотношение до 200%
            # (в реальности комментарии редко превышают 50% от лайков)
            return min(ratio, 200)
        
        filtered_df_with_like_comment_rate['likeCommentRatePercent'] = filtered_df_with_like_comment_rate.apply(
            safe_comment_rate_calculation, axis=1
        )
        
        # Создаем график Like-CommentRate
        fig_like_comment_rate = px.line(
            filtered_df_with_like_comment_rate.sort_values('timestamp'),
            x='timestamp',
            y='likeCommentRatePercent',
            title=f"Like-CommentRate по времени для аккаунта {selected_account}",
            markers=True
        )
        
        fig_like_comment_rate.update_traces(
            line=dict(color='rgb(153, 102, 255)'),
            marker=dict(color='white', size=8, line=dict(width=2, color='rgb(153, 102, 255)'))
        )
        
        fig_like_comment_rate.update_layout(
            xaxis=dict(
                rangeselector=dict(
                    buttons=[
                        dict(step="all", label="Все"),
                        dict(count=30, label="30д", step="day", stepmode="backward"),
                        dict(count=60, label="60д", step="day", stepmode="backward"),
                        dict(count=90, label="90д", step="day", stepmode="backward"),
                        dict(count=180, label="180д", step="day", stepmode="backward")
                    ]
                ),
            ),
            yaxis=dict(autorange=True, title="Like-CommentRate (%)")
        )
        
        st.plotly_chart(fig_like_comment_rate, use_container_width=True)
        
    else:
        st.warning("Нет данных о комментариях")

with tab2:
    metrics_for_plot = ['likesCount', 'commentsCount', 'videoPlayCount']
    selected_metric = st.selectbox("Выбери метрику для графика", metrics_for_plot)
    st.markdown("<br>", unsafe_allow_html=True)

    st.subheader(f"График по {selected_metric}")

    fig = px.line(
        filtered_df.sort_values('timestamp'),
        x='timestamp',
        y=selected_metric,
        title=f"{selected_metric} по времени для аккаунта {selected_account}",
        markers=True
    )

    # Красивый глубокий фиолетовый цвет для контраста с красной линией
    fig.update_traces(
        line=dict(color='rgb(102, 51, 153)'),  # Элегантный глубокий фиолетовый
        marker=dict(color='white', size=8, line=dict(width=2, color='rgb(102, 51, 153)'))
    )

    fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=[
                    dict(step="all", label="Все"),
                    dict(count=30, label="30д", step="day", stepmode="backward"),
                    dict(count=60, label="60д", step="day", stepmode="backward"),
                    dict(count=90, label="90д", step="day", stepmode="backward"),
                    dict(count=180, label="180д", step="day", stepmode="backward")
                ]
            ),
        ),
        yaxis=dict(autorange=True)  # ✅ Автоподстройка Y при изменении диапазона
    )
    
    # Добавляем горизонтальную красную линию на уровне μ + stdev_hot_threshold * σ
    metric_data = filtered_df[selected_metric].dropna()
    if len(metric_data) > 0:
        # Красная линия для HOT порога
        hot_threshold_value = metric_data.mean() + stdev_hot_treshold * metric_data.std()
        fig.add_hline(
            y=hot_threshold_value,
            line_dash="dash",
            line_color="red",
            line_width=2,
            annotation_text=f"HOT порог: μ+{stdev_hot_treshold}σ = {hot_threshold_value:,.0f}",
            annotation_position="top left"
        )
        
        # Зеленая линия для VERY SUCCESSFUL порога
        very_successful_threshold_value = metric_data.mean() + stdev_very_successful_treshold * metric_data.std()
        fig.add_hline(
            y=very_successful_threshold_value,
            line_dash="dash",
            line_color="green",
            line_width=2,
            annotation_text=f"✅ Very Successful: μ+{stdev_very_successful_treshold}σ = {very_successful_threshold_value:,.0f}",
            annotation_position="bottom left"
        )

    st.plotly_chart(fig, use_container_width=True)
    st.divider()

    # Добавляем агрегированную статистику
    st.subheader(f"Статистика по {selected_metric}")
    
    # Получаем данные для выбранной метрики
    metric_data = filtered_df[selected_metric].dropna()
    
    if len(metric_data) > 0:
        # Базовые метрики
        st.write("**Базовые метрики:**")
        
        # Создаем две колонки для базовых метрик
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Общее количество", f"{metric_data.sum():,.0f}")
            st.metric("Среднее значение", f"{metric_data.mean():,.1f}")
            st.metric("Максимум", f"{metric_data.max():,.0f}")
            st.metric("Минимум", f"{metric_data.min():,.0f}")
            
        
        with col2:
            st.metric("Медиана", f"{metric_data.median():,.1f}")
            total_video_play_count = filtered_df['videoPlayCount'].sum()
            ratio_to_total_views = (metric_data.sum() / total_video_play_count * 100) if total_video_play_count > 0 else 0
            st.metric("Отношение к общим просмотрам", f"{ratio_to_total_views:.2f}%")
            st.metric("Максимум", f"{metric_data.max():,.0f}")

        # Расширенные метрики в спойлере
        with st.expander("🔍 Расширенные метрики"):
            st.markdown("<br>", unsafe_allow_html=True)

            # Статистические выбросы
            st.write("**Статистические выбросы:**")
            
            q1 = metric_data.quantile(0.25)
            q3 = metric_data.quantile(0.75)
            iqr = q3 - q1
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("HOT-граница (μ+2σ)", f"{metric_data.mean() + stdev_hot_treshold * metric_data.std():,.1f}")
                st.metric("COLD-граница (μ-2σ)", f"{metric_data.mean() - 2 * metric_data.std():,.1f}")
                st.metric("Межквартильный размах (IQR)", f"{iqr:,.1f}")
            
            with col2:
                st.metric("Upper fence (Q3+1.5*IQR)", f"{q3 + 1.5 * iqr:,.1f}")
                st.metric("Lower fence (Q1-1.5*IQR)", f"{q1 - 1.5 * iqr:,.1f}")
            st.divider()

            # Перцентили
            st.write("**Перцентили:**")
            percentiles = [99, 90, 75, 50, 25, 10, 5]
            percentile_values = {p: metric_data.quantile(p/100) for p in percentiles}
            
            col1, col2, col3 = st.columns(3)
            for i, p in enumerate(percentiles):
                with [col1, col2, col3][i % 3]:
                    st.metric(f"{p}-й перцентиль", f"{percentile_values[p]:,.1f}")
            st.divider()
            
            # Сумма метрики в диапазонах перцентилей
            st.write(f"**Сумма {selected_metric} в диапазонах перцентилей:**")
            
            # Создаем диапазоны перцентилей
            percentile_ranges = [
                (100, 99, "100-99"),
                (99, 90, "99-90"),
                (90, 75, "90-75"),
                (75, 50, "75-50"),
                (50, 25, "50-25"),
                (25, 10, "25-10"),
                (10, 5, "10-5"),
                (5, 0, "5-0")
            ]
            
            total_sum = metric_data.sum()
            
            col1, col2 = st.columns(2)
            for i, (upper_p, lower_p, label) in enumerate(percentile_ranges):
                if upper_p == 100:
                    upper_val = metric_data.max()
                else:
                    upper_val = percentile_values[upper_p]
                
                if lower_p == 0:
                    lower_val = metric_data.min()
                else:
                    lower_val = percentile_values[lower_p]
                
                range_sum = metric_data[(metric_data >= lower_val) & (metric_data <= upper_val)].sum()
                percentage = (range_sum / total_sum * 100) if total_sum > 0 else 0
                
                with [col1, col2][i % 2]:
                    st.metric(f"Диапазон {label}%", f"{range_sum:,.0f} ({percentage:.1f}%)")
            st.divider()

            # Количество REELS в диапазонах перцентилей
            st.write("**Количество REELS в диапазонах перцентилей:**")
            
            total_count = len(metric_data)
            
            col1, col2 = st.columns(2)
            for i, (upper_p, lower_p, label) in enumerate(percentile_ranges):
                if upper_p == 100:
                    upper_val = metric_data.max()
                else:
                    upper_val = percentile_values[upper_p]
                
                if lower_p == 0:
                    lower_val = metric_data.min()
                else:
                    lower_val = percentile_values[lower_p]
                
                range_count = len(metric_data[(metric_data >= lower_val) & (metric_data <= upper_val)])
                count_percentage = (range_count / total_count * 100) if total_count > 0 else 0
                
                with [col1, col2][i % 2]:
                    st.metric(f"Диапазон {label}%", f"{range_count} ({count_percentage:.1f}%)")
            st.divider()
            
            # Метрики устойчивости
            st.write("**Метрики устойчивости:**")
            
            coefficient_of_variation = metric_data.std() / metric_data.mean()
            skewness = metric_data.skew()
            kurtosis = metric_data.kurtosis()
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Коэффициент вариации", f"{coefficient_of_variation:.3f}")
            with col2:
                st.metric("Асимметрия (skewness)", f"{skewness:.3f}")
            with col3:
                st.metric("Эксцесс (kurtosis)", f"{kurtosis:.3f}")
    
        
        # Фильтрация по mark-параметрам
        st.subheader("Фильтры видео")
        
        # Определяем какой mark-параметр использовать в зависимости от выбранной метрики
        mark_mapping = {
            'likesCount': 'markLikes',
            'commentsCount': 'markComments', 
            'videoPlayCount': 'markPlay'
        }
        
        mark_column = mark_mapping[selected_metric]
        
        # Получаем все возможные значения категорий
        category_options = ['🔥viral hit', '✅very successful', 'successful', 'average', 'weak']
        
        # Фильтр с предустановленным значением '🔥viral hit'
        selected_categories = st.multiselect(
            f"Фильтр по категории ({mark_column})",
            options=category_options,
            default=['🔥viral hit']
        )
        
                # Фильтруем данные по выбранным категориям
        if selected_categories:
            filtered_videos_df = filtered_df[filtered_df[mark_column].isin(selected_categories)]
        else:
            filtered_videos_df = filtered_df
        
        # Видео карточки с применением всех фильтров
        st.divider()
        st.subheader("Видео карточки")
        
        if len(filtered_videos_df) > 0:
            for i in range(0, len(filtered_videos_df), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    if i + j < len(filtered_videos_df):
                        row = filtered_videos_df.iloc[i + j]
                        with col:
                            st.markdown(f"**📹 `{row['url']}`**")
                            st.video(row['videoUrl'])
                            st.caption(f"👁 {int(row['videoPlayCount'])} | ❤️ {int(row['likesCount'])} | {row[mark_column]}")
        else:
            st.info("Нет видео, соответствующих выбранным фильтрам")
    
    else:
        st.warning("Нет данных для выбранной метрики")
