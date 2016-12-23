function getInitialState() {
  return {
    article: {
      text: ""
    },
    saveAndNext: null
  };
}

const initialState = Object.assign({
  article: {},
}, getInitialState());


export function article(state = initialState, action) {
  switch (action.type) {
    case 'FETCH_ARTICLE':
      return {
        ...state,
        article: {
          isFetching: true,
          text: ""
        },
      }
    case 'FETCH_ARTICLE_SUCCESS':
      return {
        ...state,
        article: action.response
      }
    case 'POST_HIGHLIGHTS_CALLBACK':
      return {
        ...state,
        saveAndNext: action.saveAndNext
      }
    case 'POST_HIGHLIGHTS':
      return state
    default:
      return state;
  }
}
