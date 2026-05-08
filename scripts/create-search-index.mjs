import { getCollection } from 'astro:content';
import fs from 'fs';
import path from 'path';

const OUTPUT_DIR = 'public';
const OUTPUT_FILE = 'search-index.json';

export default async function createSearchIndex() {
  console.log('Creating search index...');

  try {
    const allPosts = await getCollection('blog');

    const searchIndex = allPosts.map(post => ({
      id: post.id,
      url: `/${post.id}`,
      title: post.data.title,
      description: post.data.description,
      category: post.data.category || '',
      date: post.data.pubDate.toISOString(),
      // Add first 500 characters of content for better search
      content: post.body?.slice(0, 500) || ''
    }));

    // Ensure output directory exists
    const outputPath = path.join(process.cwd(), OUTPUT_DIR, OUTPUT_FILE);
    const outputDir = path.dirname(outputPath);

    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    // Write search index
    fs.writeFileSync(outputPath, JSON.stringify(searchIndex, null, 2));

    console.log(`✅ Search index created with ${searchIndex.length} articles`);
    console.log(`📁 Location: ${outputPath}`);

    return searchIndex;
  } catch (error) {
    console.error('❌ Error creating search index:', error);
    throw error;
  }
}