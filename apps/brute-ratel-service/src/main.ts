/**
 * Brute Ratel C4 Community Kit Service
 * Security toolkit with scripts, BOFs, and utilities for Brute Ratel C4
 */

import { startServer } from './app/app';

const port = parseInt(process.env['PORT'] || '3333', 10);
startServer(port);
