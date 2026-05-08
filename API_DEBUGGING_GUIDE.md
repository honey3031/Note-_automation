# API 405 Error Debugging Guide

## Problem
The API is returning **405 Method Not Allowed** when attempting to POST to `/notes` endpoint.

## Root Causes to Investigate

### 1. Endpoint Path Issue
- Current: `https://practice.expandtesting.com/notes/api/notes`
- Should verify actual endpoint in API docs

**Solution**: Test with Postman
```
POST https://practice.expandtesting.com/notes/api/notes
Headers: 
  - x-auth-token: <your_token>
  - Content-Type: application/json
Body:
{
  "title": "Test Note",
  "description": "Test Description",
  "category": "Home"
}
```

### 2. Missing Required Headers
The API might require additional headers beyond `x-auth-token`.

**Common headers to try**:
```
- Content-Type: application/json
- Accept: application/json
- Authorization: Bearer <token>
```

### 3. API Authentication Issue
The token might be invalid or expired.

**Check**: Verify login is working correctly by checking login response.

### 4. API Endpoint Version
The endpoint might have a version prefix.

**Try these variants**:
```
POST https://practice.expandtesting.com/notes/api/v1/notes
POST https://practice.expandtesting.com/notes/api/notes/create
POST https://practice.expandtesting.com/api/notes
```

## Steps to Debug

### Step 1: Test Login Endpoint
```bash
curl -X POST https://practice.expandtesting.com/notes/api/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"your@email.com","password":"password"}'
```

### Step 2: Test Create Endpoint with Token
```bash
# Get token from login
TOKEN=<your_token_from_step1>

curl -X POST https://practice.expandtesting.com/notes/api/notes \
  -H "Content-Type: application/json" \
  -H "x-auth-token: $TOKEN" \
  -d '{"title":"Test","description":"Test","category":"Home"}'
```

### Step 3: Check API Documentation
Visit: https://practice.expandtesting.com/notes/api/api-docs/

Look for:
- Exact endpoint paths
- Required HTTP methods
- Required headers
- Request body format
- Response format

## Temporary Workaround

If API creation doesn't work, you can:
1. Skip API creation tests temporarily
2. Focus on UI-only tests
3. Test API GET endpoint (which appears to be working)

## Notes
- The GET `/notes` endpoint appears to be working (returning 200)
- Login endpoint is working (returning 200)
- Only POST to `/notes` is returning 405
- This suggests the API might only support GET for notes, not POST
