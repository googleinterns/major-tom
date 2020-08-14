const articles = [
  {
    id: '1',
    number: 1,
    content:
            'Esta prohibido manejar en las siguientes condiciones:\n\t 1. Teniendo los faros rotos\n\t 2. Teniendo las llantas ponchadas\nCualquiera de estos casos no será tolerado!',
    keywords: [
      'Lorem',
      'Ipsum',
      'Ipsum',
      'Ipsum',
      'Ipsum',
      'Ipsum',
      'Ipsum',
      'Ipsum',
      'Ipsum',
      'Ipsum'
    ],
    wordCount: 1125
  },
  {
    id: '2',
    number: 2,
    content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    keywords: ['Lorem', 'Ipsum'],
    wordCount: 2250
  },
  {
    id: '3',
    number: 3,
    content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    keywords: ['Lorem', 'Ipsum'],
    wordCount: 1800
  },
  {
    id: '4',
    number: 4,
    content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    keywords: ['Lorem', 'Ipsum'],
    wordCount: 540
  },
  {
    id: '5',
    number: 5,
    content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    keywords: ['Lorem', 'Ipsum'],
    wordCount: 355
  },
  {
    id: '6',
    number: 6,
    content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    keywords: ['Lorem', 'Ipsum'],
    wordCount: 355
  },
  {
    id: '7',
    number: 7,
    content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    keywords: ['Lorem', 'Ipsum'],
    wordCount: 355
  },
  {
    id: '8',
    number: 8,
    content:
            'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
    keywords: ['Lorem', 'Ipsum'],
    wordCount: 800
  }
]

const responses = {
  articleIdsFromSearch: limit => {
    const articles = []

    for (let i = 1; i <= limit; i++) {
      articles.push(i)
    }

    return { data: { articles } }
  },
  errorResponseFromSearch: () => ({ error: { message: 'This is the error message', trace: 'unicode ugly stack trace' } }),
  articleFromIdDatabase: id => {
    for (const article of articles) {
      if (parseInt(article.id) === id) { return article }
    }

    return { error: 'No article matches such ID', code: 404 }
  }
}

export { responses, articles }
