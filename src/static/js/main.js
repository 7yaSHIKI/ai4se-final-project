// 刷新所有订阅源
async function refreshFeeds() {
    const btn = event.target;
    const originalText = btn.textContent;
    btn.disabled = true;
    btn.textContent = '⏳ 刷新中...';

    try {
        const response = await fetch('/api/refresh', {method: 'POST'});
        const result = await response.json();

        if (result.success) {
            alert(`刷新完成！\n新增文章：${result.new_articles} 篇\n成功：${result.success_count} 个\n失败：${result.failed_count} 个`);
            location.reload();
        } else {
            alert('刷新失败');
        }
    } catch (error) {
        alert('刷新失败：' + error.message);
    } finally {
        btn.disabled = false;
        btn.textContent = originalText;
    }
}

// 标签筛选
document.addEventListener('DOMContentLoaded', () => {
    const filterBtns = document.querySelectorAll('.filter-btn');
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tag = btn.dataset.tag;
            const url = tag ? `/?tag=${encodeURIComponent(tag)}` : '/';
            window.location.href = url;
        });
    });
});
