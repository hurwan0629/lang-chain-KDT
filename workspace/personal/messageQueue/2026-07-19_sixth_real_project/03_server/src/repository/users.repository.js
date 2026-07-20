import pool from "../config/db.js";
import logger from "../utils/logger.js";

export async function getUserById(id) {
  try {
    const result = await pool.query(`
      SELECT 
        pk, id, name, 
        password_hash as "passwordHash",  
        role, email, address, 
        created_at as "createdAt", 
        updated_at as "updatedAt"
      FROM 
        users
      WHERE
        id = $1
        AND deleted_at IS NOT NULL
      `, [id])
    
    return result.rows[0] ?? null
  } catch (error) {
    logger("/repository/users.repository.js getUserById",
      `error: ${error}`
    )
    throw error
  }
}