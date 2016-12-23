export function postArticleHighlights(highlightsString, articleId) {
  return (dispatch) => {
    dispatch({ type: 'POST_HIGHLIGHTS'});

    return fetch(`http://localhost:5000/api/postHighlights/${articleId}`, {
        method: 'POST',
        body: highlightsString
      })
      .then(response => response.json())
      .then(
        (response) => dispatch({ type: 'POST_HIGHLIGHTS_SUCCESS'}, response),
        (error) => dispatch({ type: 'POST_HIGHLIGHTS_FAIL', error})
      );
  };
}

export function storeArticle(article) {
  return {
    type: 'FETCH_ARTICLE_SUCCESS',
    response: article
  };
}

export function storeSaveAndNext(saveAndNext) {
  return {
    type: 'POST_HIGHLIGHTS_CALLBACK',
    saveAndNext: saveAndNext
  };
}
