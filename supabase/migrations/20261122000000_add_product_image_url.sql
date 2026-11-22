-- Migration: 20261122000000_add_product_image_url.sql
-- Description: Add image_url column to products table for POS and external store synchronization

ALTER TABLE products 
ADD COLUMN IF NOT EXISTS image_url TEXT;

COMMENT ON COLUMN products.image_url IS 'Product display image URL fetched from store/website integrations or uploaded';
