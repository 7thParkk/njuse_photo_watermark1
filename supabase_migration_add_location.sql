-- 迁移脚本：为 travel_plans 表添加 location 列
-- 如果您的数据库已经创建，请运行此脚本来添加 location 列

-- 添加 location 列（如果不存在）
DO $$ 
BEGIN
  IF NOT EXISTS (
    SELECT 1 
    FROM information_schema.columns 
    WHERE table_name = 'travel_plans' 
    AND column_name = 'location'
  ) THEN
    ALTER TABLE travel_plans ADD COLUMN location JSONB;
    RAISE NOTICE 'Column location added to travel_plans table';
  ELSE
    RAISE NOTICE 'Column location already exists in travel_plans table';
  END IF;
END $$;

