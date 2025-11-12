// Constants shared across Mealie applications
export const API_ROUTES = {
  // Authentication
  AUTH: {
    LOGIN: '/api/auth/token',
    REFRESH: '/api/auth/refresh',
    LOGOUT: '/api/auth/logout',
  },
  
  // Recipes
  RECIPES: {
    BASE: '/api/recipes',
    SEARCH: '/api/recipes/search',
    RANDOM: '/api/recipes/random',
    BY_SLUG: (slug: string) => `/api/recipes/${slug}`,
    IMAGE: (id: string) => `/api/media/recipes/${id}/images/original.webp`,
    THUMBNAIL: (id: string) => `/api/media/recipes/${id}/images/min-original.webp`,
  },
  
  // Users
  USERS: {
    BASE: '/api/users',
    SELF: '/api/users/self',
    BY_ID: (id: string) => `/api/users/${id}`,
  },
  
  // Groups
  GROUPS: {
    BASE: '/api/groups',
    SELF: '/api/groups/self',
  },
  
  // Meal Plans
  MEAL_PLANS: {
    BASE: '/api/groups/mealplans',
    BY_DATE: (date: string) => `/api/groups/mealplans/${date}`,
  },
  
  // Shopping Lists
  SHOPPING_LISTS: {
    BASE: '/api/groups/shopping/lists',
    ITEMS: '/api/groups/shopping/items',
  }
} as const;

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  UNAUTHORIZED: 401,
  FORBIDDEN: 403,
  NOT_FOUND: 404,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500,
  NOT_IMPLEMENTED: 501,
} as const;

export const DEFAULT_SETTINGS = {
  RECIPES_PER_PAGE: 20,
  MAX_FILE_SIZE_MB: 100,
  SUPPORTED_IMAGE_FORMATS: ['jpg', 'jpeg', 'png', 'webp'],
  DEFAULT_RECIPE_IMAGE: '/images/default-recipe.jpg',
} as const;

export const VALIDATION = {
  MIN_PASSWORD_LENGTH: 8,
  MAX_RECIPE_NAME_LENGTH: 255,
  MAX_TAG_NAME_LENGTH: 50,
  MAX_INGREDIENT_NAME_LENGTH: 100,
} as const;

export const DEFAULT_PORTS = {
  INTEGRATION_SERVICE: 9925,
  API_SERVICE: 9000,
  WEB_SERVICE: 3000,
} as const;

export const DEFAULT_PATHS = {
  WEB_OUTPUT: './apps/mealie-web/.output/public',
  DATA_DIR: './data',
  BACKUP_DIR: './backups',
} as const;